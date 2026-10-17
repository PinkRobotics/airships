"""Nonresponse mechanics and deterministic toy-controller checks only.

No test solves the shell equilibrium or uses the source-pressure comparator.
Physical energy derivatives are checked at fixed synthetic non-equilibrium states.
"""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import vacuum_u1_hutchinson_controller as control
import vacuum_u1_hutchinson_mechanics as mechanics
import vacuum_u1_hutchinson_job as job


class MemoryAudit:
    def __init__(self):
        self.events = []

    def event(self, event, **data):
        self.events.append(dict(event=event, **data))

    def arrays(self, label, **values):
        return dict(label=label, **{key: np.array(value, copy=True) for key, value in values.items()})


def no_deadline():
    pass


class Parabola:
    """Artificial two-variable curve with a known maximum, unrelated to a shell."""
    n_unknowns = 2
    p_c = 1.0
    peak_q = 0.623417

    def target(self, q):
        return np.array([0.1*q, q*(2*self.peak_q-q)])

    def evaluate(self, x, q, jacobian=True):
        f = x - self.target(q)
        return (float(f@f/2), f, np.eye(2) if jacobian else None,
                -np.array([0.1, 2*(self.peak_q-q)]) if jacobian else None)

    def sample(self, x, q):
        return np.array([q, x[-1], x[0]])


def toy_state(q, pressure, slope, field=0.0, field_slope=0.0, correction=0.0):
    return control.State(q, np.array([field, pressure]), np.array([0.0, correction]),
                         np.array([field_slope, slope]), np.array([q, pressure, field]),
                         np.array([1.0, slope, field_slope]), np.zeros(2), {})


class MechanicsChecks(unittest.TestCase):
    def test_natural_cardinal_and_integral_operators_at_frozen_meshes(self):
        for n in (64, 128, 256):
            with self.subTest(intervals=n):
                op = mechanics.Operators(n)
                values = op.spline(op.nodes)
                np.testing.assert_allclose(values[1:-1], np.eye(n-1), rtol=0, atol=2e-14)
                np.testing.assert_allclose(values[[0, -1]], 0, rtol=0, atol=2e-14)
                np.testing.assert_allclose(op.spline([0, mechanics.END], 2),
                                           0, rtol=0, atol=1e-8)
                shape, _, integral = op.at(op.points)
                numerical = op.weights @ shape
                exact = op.primitive(mechanics.END) - op.primitive(0)
                np.testing.assert_allclose(numerical, exact, rtol=1e-12, atol=2e-15)
                np.testing.assert_allclose(op.at([mechanics.END])[2], 0, atol=0)
                self.assertEqual(len(op.samples), 17*n+1)
                self.assertTrue(np.all(np.diff(op.samples) > 0))
                self.assertTrue(np.all(op.points > 0))
                self.assertTrue(np.all(op.points < mechanics.END))
                self.assertTrue(np.all(np.isfinite(integral)))
                for degree in (0, 1, 2, 7, 15):
                    self.assertAlmostEqual(float(op.weights @ op.points**degree)
                                           / (mechanics.END**(degree+1)/(degree+1)),
                                           1, places=13)

    def test_analytic_energy_gradient_and_hessian_by_complex_step(self):
        shell = mechanics.Shell(8)
        a = 0.0007*np.sin(np.arange(shell.n_unknowns)+0.37)
        pressure = 0.137
        energy, f, h = shell.original(a, pressure)
        self.assertGreater(np.linalg.norm(f, np.inf), 1e-5)  # Not an equilibrium.
        step = 1e-30
        gradient = np.empty_like(f)
        hessian = np.empty_like(h)
        for i in range(len(a)):
            trial = a.astype(complex)
            trial[i] += 1j*step
            e, residual, _ = shell.original(trial, pressure, hessian=False)
            gradient[i] = e.imag/step
            hessian[:, i] = residual.imag/step
        np.testing.assert_allclose(gradient, f, rtol=2e-12, atol=2e-14)
        np.testing.assert_allclose(hessian, h, rtol=3e-11, atol=2e-13)
        np.testing.assert_allclose(h, h.T, rtol=2e-12, atol=2e-13)
        self.assertTrue(np.isfinite(energy))

    def test_scaled_jacobian_and_q_derivative_keep_original_pole_row(self):
        shell = mechanics.Shell(8)
        x = 0.02*np.cos(np.arange(shell.n_unknowns)+0.41)
        x[-1] = 0.119
        q = 0.173
        _, f, j, fq = shell.evaluate(x, q)
        step = 1e-30
        numeric = np.empty_like(j)
        for i in range(len(x)):
            trial = x.astype(complex)
            trial[i] += 1j*step
            numeric[:, i] = shell.evaluate(trial, q, jacobian=False)[1].imag/step
        np.testing.assert_allclose(j, numeric, rtol=2e-11, atol=2e-14)
        numeric_q = shell.evaluate(x, q+1j*step, jacobian=False)[1].imag/step
        np.testing.assert_allclose(fq, numeric_q, rtol=2e-11, atol=2e-14)
        a = np.r_[mechanics.EPSILON*x[:-1], -mechanics.EPSILON*q]
        _, original_f, h = shell.original(a, x[-1])
        np.testing.assert_array_equal(f, original_f)
        np.testing.assert_allclose(j[:, :-1], mechanics.EPSILON*h[:, :-1], atol=0)
        np.testing.assert_allclose(fq, -mechanics.EPSILON*h[:, -1], atol=0)
        # dPsi/dlambda is a load potential, not the retained Wp stationarity row.
        self.assertNotAlmostEqual(f[-1], shell.load@a, places=7)

    def test_pole_coordinate_has_closed_form_membrane_and_dead_load_derivatives(self):
        shell = mechanics.Shell(8)
        a = np.zeros(shell.n_unknowns)
        a[-1] = -0.00083
        pressure = 0.091
        energy, f, h = shell.original(a, pressure)
        area = shell.weights.sum()
        expected_energy = area*(a[-1]**2/(1-mechanics.NU)
                                + mechanics.GAMMA*pressure*a[-1])
        self.assertAlmostEqual(energy, expected_energy, places=17)
        self.assertAlmostEqual(f[-1], area*(2*a[-1]/(1-mechanics.NU)
                                            + mechanics.GAMMA*pressure), places=15)
        self.assertAlmostEqual(h[-1, -1], area*2/(1-mechanics.NU), places=13)
        self.assertAlmostEqual(shell.load[-1], area*mechanics.GAMMA, places=15)

    def test_sample_operator_and_tangent_are_linear_with_exact_pole_value(self):
        shell = mechanics.Shell(8)
        x = .01*np.sin(np.arange(shell.n_unknowns)+.2)
        direction = .03*np.cos(np.arange(shell.n_unknowns)+.1)
        q, h = .27, .013
        z = shell.sample(x, q)
        t = shell.sample(direction, 1)
        np.testing.assert_allclose(shell.sample(x+h*direction, q+h), z+h*t,
                                   rtol=1e-13, atol=1e-15)
        self.assertEqual(z[-1], -q)
        np.testing.assert_allclose(z[[-3, -2]], 0, atol=1e-15)
        self.assertEqual(t[0], 1)


class ControllerChecks(unittest.TestCase):
    def setUp(self):
        self.audit = MemoryAudit()
        self.controller = control.Continuation(Parabola(), self.audit, no_deadline)

    def test_toy_peak_complete_trace_and_no_extra_refinement(self):
        result = self.controller.run()
        self.assertEqual(result['status'], 'CERTIFIED_NUMERICAL_PEAK')
        self.assertLessEqual(result['bracket'][0], Parabola.peak_q)
        self.assertGreaterEqual(result['bracket'][1], Parabola.peak_q)
        self.assertLessEqual(result['bracket'][1]-result['bracket'][0], .001)
        self.assertLess(abs(result['peak']-Parabola.peak_q**2), 1e-6)
        self.assertEqual(len(result['descending']), 3)
        self.assertTrue(all(s['slope'] < -1e-8 for s in result['descending']))
        attempts = [e for e in self.audit.events if e['event'] == 'attempt']
        self.assertEqual(len({e['q'] for e in attempts}), len(attempts))
        self.assertLessEqual(result['refinements'], 24)
        self.assertLessEqual(result['attempts'], 125)
        self.assertEqual(attempts[0]['q'], 0)
        self.assertIsNone(attempts[0]['seed_q'])
        accepted = []
        for event in self.audit.events:
            if event['event'] == 'attempt' and event['q'] not in [j/20 for j in range(101)]:
                selected = min(accepted, key=lambda q: (abs(event['q']-q), q))
                self.assertEqual(event['seed_q'], selected)
            elif event['event'] == 'accepted':
                accepted.append(event['q'])
        neighbors = [e for e in self.audit.events if e['event'] == 'neighbor_branch_check']
        for event in attempts:
            if event['q'] not in [j/20 for j in range(101)]:
                self.assertEqual(sum(e['q'] == event['q'] for e in neighbors), 2)

    def test_lu_condition_guard_and_every_rhs_residual(self):
        j = np.array([[3.0, 2.0], [1.0, 4.0]])
        system = control.LinearSystem(j)
        result, error = system.solve(np.array([7.0, 9.0]))
        np.testing.assert_allclose(j@result, [7, 9], atol=2e-15)
        self.assertLessEqual(error, 1e-12)
        zero, error = system.solve(np.zeros(2))
        np.testing.assert_array_equal(zero, 0)
        self.assertEqual(error, 0)
        for invalid in (np.diag([1.0, 1e-13]), np.zeros((2, 2)), np.diag([1.0, np.nan])):
            with self.subTest(matrix=invalid), self.assertRaisesRegex(control.Unresolved, 'JACOBIAN'):
                control.LinearSystem(invalid)

    def test_zero_failure_has_one_evaluation_and_no_update(self):
        class BadZero(Parabola):
            def target(self, q):
                return super().target(q)+.01
        controller = control.Continuation(BadZero(), self.audit, no_deadline)
        with self.assertRaisesRegex(control.Unresolved, 'ZERO_STATE'):
            controller.solve(0)
        self.assertEqual(controller.attempts, 1)
        self.assertEqual(controller.cache, {})
        self.assertEqual(sum(e['event'] == 'iteration' for e in self.audit.events), 1)
        self.assertFalse(any(e['event'] == 'trial' for e in self.audit.events))

    def test_same_iterate_uses_undamped_correction_not_residual_alone(self):
        class TinyResidual(Parabola):
            def evaluate(self, x, q, jacobian=True):
                f = np.array([5e-11, 0.0])
                return 0.0, f, 1e-3*np.eye(2), np.array([0.0, -.001])
        controller = control.Continuation(TinyResidual(), self.audit, no_deadline)
        with self.assertRaisesRegex(control.Unresolved, 'ZERO_STATE'):
            controller.solve(0)
        event = next(e for e in self.audit.events if e['event'] == 'iteration')
        self.assertLessEqual(event['residual_inf'], 1e-10)
        self.assertGreater(event['undamped_relative_inf'], 1e-9)

    def test_twenty_current_evaluations_allow_only_nineteen_updates(self):
        class SlowCorrector(Parabola):
            """Deliberately inaccurate toy tangent exercises the controller cap."""
            def evaluate(self, x, q, jacobian=True):
                e, f, j, fq = super().evaluate(x, q, jacobian)
                return e, f, 100*j if jacobian else None, fq
        model = SlowCorrector()
        controller = control.Continuation(model, self.audit, no_deadline)
        x = np.zeros(2)
        with self.assertRaisesRegex(control.Unresolved, 'NEWTON_BUDGET'):
            controller.iterate(.1, x, False, model.sample(x, .1), 10)
        self.assertEqual(sum(e['event'] == 'iteration' for e in self.audit.events), 20)
        trials = [e for e in self.audit.events if e['event'] == 'trial']
        self.assertEqual(len(trials), 19)
        self.assertTrue(all(e['alpha'] == 1 for e in trials))

    def test_exact_eight_armijo_factors_no_ninth_or_new_direction(self):
        class NoDecrease(Parabola):
            def evaluate(self, x, q, jacobian=True):
                if not jacobian:
                    return 1.0, np.ones(2), None, None
                return super().evaluate(x, q, jacobian)
        model = NoDecrease()
        controller = control.Continuation(model, self.audit, no_deadline)
        x = np.zeros(2)
        with self.assertRaisesRegex(control.Unresolved, 'BACKTRACKING'):
            controller.iterate(.1, x, False, model.sample(x, .1), 10)
        trials = [e for e in self.audit.events if e['event'] == 'trial']
        self.assertEqual([e['alpha'] for e in trials], list(control.ALPHAS))
        self.assertTrue(all(e['reason'] == 'armijo' for e in trials))

    def test_fixed_tube_rejects_sampled_displacement_without_recentering(self):
        x = np.array([0.0, .1])
        prediction = self.controller.model.sample(x, .1)
        inside, _, _ = self.controller.tube(x+np.array([.02, 0]), .1, prediction, .01)
        self.assertFalse(inside)
        inside, _, _ = self.controller.tube(x+np.array([np.nan, 0]), .1, prediction, .01)
        self.assertFalse(inside)

    def test_both_neighbors_checked_and_bad_right_neighbor_is_terminal(self):
        left = toy_state(0, 0, 1)
        right = toy_state(.1, .1, 1, field_slope=10)
        self.controller.cache = {0: left, .1: right}
        with self.assertRaisesRegex(control.Unresolved, 'BRANCH'):
            self.controller.branch_checks(toy_state(.05, .05, 1))
        events = [e for e in self.audit.events if e['event'] == 'neighbor_branch_check']
        self.assertEqual([e['neighbor_q'] for e in events], [0, .1])

    def test_pressure_comparison_retains_correction_margin_and_refuses_tie(self):
        a = toy_state(.2, 1, 1, correction=1e-9)
        b = toy_state(.3, 1+1e-9, -1)
        with self.assertRaisesRegex(control.Unresolved, 'PRESSURE_TIE'):
            self.controller.compare(a, b, 'fixture')
        b.x[-1] = 1+1e-6
        self.assertEqual(self.controller.compare(a, b, 'fixture'), 1)
        self.assertEqual(self.controller.compare(b, a, 'fixture'), -1)

    def test_neutral_endpoint_cannot_certify_peak(self):
        a, m, b = toy_state(0, 0, 0), toy_state(.1, 1, 0), toy_state(.2, 0, -1)
        self.controller.cache = {s.q: s for s in (a, m, b)}
        with self.assertRaisesRegex(control.Unresolved, 'PEAK_BRACKET'):
            self.controller.bracket(a, b)

    def test_negative_to_positive_slope_is_never_an_alternate_peak(self):
        a = toy_state(0, 1, -1e-6)
        self.controller.cache = {0: a}
        with self.assertRaisesRegex(control.Unresolved, 'MULTIPLE_TURNING'):
            self.controller.branch_checks(toy_state(.05, 1, 1e-6))

    def test_monotonic_toy_hits_fixed_q_ceiling_without_invented_peak(self):
        class Monotonic(Parabola):
            def target(self, q):
                return np.array([.1*q, q])
            def evaluate(self, x, q, jacobian=True):
                f = x-self.target(q)
                return float(f@f/2), f, np.eye(2), -np.array([.1, 1.0])
        controller = control.Continuation(Monotonic(), self.audit, no_deadline)
        with self.assertRaisesRegex(control.Unresolved, 'Q_CEILING'):
            controller.run()
        self.assertEqual(controller.attempts, 101)
        self.assertEqual(max(controller.cache), 5)
        self.assertEqual(controller.refinements, 0)

    def test_attempt_cap_collision_and_refinement_cap_do_not_solve_again(self):
        self.controller.attempts = 126
        with self.assertRaisesRegex(control.Unresolved, 'REFINEMENT_BUDGET'):
            self.controller.solve(0)
        self.assertEqual(self.controller.attempts, 126)
        self.controller.attempts = 0
        a, b = toy_state(0, 0, 1), toy_state(1, 0, -1)
        self.controller.cache = {0: a, 1: b}
        with self.assertRaisesRegex(control.Unresolved, 'Q_COLLISION'):
            self.controller.new_refinement(0, a, b)
        self.controller.refinements = 24
        with self.assertRaisesRegex(control.Unresolved, 'REFINEMENT_BUDGET'):
            self.controller.new_refinement(.5, a, b)
        self.assertEqual(self.controller.attempts, 0)

    def test_first_mesh_failure_prevents_all_later_models(self):
        seen = []
        def factory(n):
            seen.append(n)
            raise control.Unresolved('UNRESOLVED_TOY_FIXTURE')
        result = control.sequence(factory, self.audit, no_deadline)
        self.assertEqual(result['status'], 'UNRESOLVED')
        self.assertEqual(seen, [64])
        self.assertEqual(result['completed_meshes'], [])

    def test_expired_deadline_never_reserves_a_state(self):
        controller = control.Continuation(Parabola(), self.audit, control.Deadline(0))
        with self.assertRaisesRegex(control.Unresolved, 'WALL_BUDGET'):
            controller.solve(0)
        self.assertEqual(controller.attempts, 0)


class LaunchGuardChecks(unittest.TestCase):
    """Pure clock/scope fixtures; no response launcher or physical solve runs."""

    def test_setup_and_shutdown_share_the_single_total_deadline(self):
        window = job.launch_window(100.0, 137.25)
        self.assertEqual(window['total_deadline'], 7300.0)
        self.assertEqual(window['response_deadline'], 7288.0)
        self.assertEqual(window['scope_seconds'], 7150)
        self.assertEqual(window['timeout_seconds'], 7148)
        self.assertEqual(window['cleanup_reserved_seconds'], 12)
        self.assertLessEqual(137.25+window['scope_seconds']+12, 7300.0)
        self.assertLess(window['timeout_seconds']+1, window['scope_seconds'])

    def test_exhausted_setup_cannot_reset_or_launch_a_new_deadline(self):
        for current in (7285.01, 7288.0, 7301.0):
            with self.subTest(now=current), self.assertRaisesRegex(RuntimeError, 'exhausted'):
                job.launch_window(100.0, current)

    def test_only_measured_inactive_scope_with_empty_cgroup_is_clear(self):
        self.assertTrue(job.inactive({'ActiveState': 'inactive', 'ControlGroup': ''}))
        for fields in ({}, {'ActiveState': 'inactive'},
                       {'ActiveState': 'inactive', 'ControlGroup': '/live'},
                       {'ActiveState': 'active', 'ControlGroup': ''},
                       {'ActiveState': 'deactivating', 'ControlGroup': ''}):
            with self.subTest(fields=fields):
                self.assertFalse(job.inactive(fields))

    def test_scope_query_failure_is_not_an_inactive_receipt(self):
        result = SimpleNamespace(returncode=1, stdout='', stderr='fixture bus unavailable')
        with patch.object(job.subprocess, 'run', return_value=result) as run:
            with self.assertRaisesRegex(RuntimeError, 'Cannot measure scope'):
                job.scope_status('fixture-only')
            self.assertEqual(run.call_args.kwargs['timeout'], 3)


if __name__ == '__main__':
    unittest.main()
