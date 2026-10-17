"""Deterministic protocol86b6abca continuation; first failure is terminal.

The controller has no access to source comparators or another mesh's response.
Toy models can exercise these guards without tracing a physical shell.
"""

from dataclasses import dataclass
import math
import time

import numpy as np
from scipy.linalg.lapack import dgecon, dgetrf, dgetrs


ALPHAS = tuple(2.0**-k for k in range(8))
SLOPE_TOL = 1e-8


class Unresolved(RuntimeError):
    def __init__(self, reason, **details):
        super().__init__(reason)
        self.reason = reason
        self.details = details


def require(condition, reason, **details):
    if not condition:
        raise Unresolved(reason, **details)


def finite(*values):
    return all(np.all(np.isfinite(v)) for v in values)


def infnorm(value):
    return float(np.max(np.abs(value)))


def sign(slope):
    return 1 if slope > SLOPE_TOL else (-1 if slope < -SLOPE_TOL else 0)


class Deadline:
    def __init__(self, deadline):
        self.deadline = deadline

    def __call__(self):
        require(time.monotonic() < self.deadline, "UNRESOLVED_WALL_BUDGET")


class LinearSystem:
    """One partial-pivot factorization, condition estimate and checked RHSs."""

    def __init__(self, j):
        require(finite(j), "UNRESOLVED_JACOBIAN", detail="nonfinite matrix")
        self.j = j
        self.norm = float(np.linalg.norm(j, np.inf))
        norm1 = float(np.linalg.norm(j, 1))
        self.lu, self.pivots, info = dgetrf(j, overwrite_a=False)
        require(info == 0 and finite(self.lu), "UNRESOLVED_JACOBIAN", lu_info=int(info))
        self.rcond, info = dgecon(self.lu, norm1, norm="1")
        require(info == 0 and finite(self.rcond, self.norm, norm1)
                and self.rcond > 1e-12, "UNRESOLVED_JACOBIAN",
                rcond1=self.rcond, condition_info=int(info))

    def solve(self, rhs):
        require(finite(rhs), "UNRESOLVED_LINEAR_RESIDUAL", detail="nonfinite rhs")
        v, info = dgetrs(self.lu, self.pivots, rhs, overwrite_b=False)
        numerator = infnorm(self.j @ v - rhs)
        denominator = self.norm * infnorm(v) + infnorm(rhs)
        ratio = numerator / denominator if denominator else (0.0 if not numerator else math.inf)
        require(info == 0 and finite(v, numerator, denominator, ratio) and ratio <= 1e-12,
                "UNRESOLVED_LINEAR_RESIDUAL", ratio=ratio, solve_info=int(info))
        return v, ratio


@dataclass
class State:
    q: float
    x: np.ndarray
    correction: np.ndarray
    xq: np.ndarray
    z: np.ndarray
    tangent: np.ndarray
    residual: np.ndarray
    diagnostics: dict

    @property
    def pressure(self):
        return float(self.x[-1])

    @property
    def slope(self):
        return float(self.xq[-1])


class Continuation:
    def __init__(self, model, audit, budget):
        self.model, self.audit, self.budget = model, audit, budget
        self.cache = {}
        self.coarse = []
        self.attempts = 0
        self.refinements = 0
        self.peaks = []

    def emit(self, event, **data):
        self.budget()
        self.audit.event(event, **data)

    def compare(self, i, j, purpose):
        """Return sign(lambda_j-lambda_i), refusing an unresolved comparison."""
        margin = (10 * (abs(i.correction[-1]) + abs(j.correction[-1]))
                  + 64 * 2.0**-52 * max(1, abs(i.pressure), abs(j.pressure)))
        difference = j.pressure - i.pressure
        self.emit("pressure_comparison", purpose=purpose, qi=i.q, qj=j.q,
                  difference=difference, margin=margin)
        require(finite(difference, margin) and abs(difference) > margin,
                "UNRESOLVED_PRESSURE_TIE", purpose=purpose, qi=i.q, qj=j.q,
                difference=difference, margin=margin)
        return 1 if difference > 0 else -1

    def neighbors(self, state):
        qs = sorted(self.cache)
        lower = [q for q in qs if q < state.q]
        upper = [q for q in qs if q > state.q]
        return [self.cache[q] for q in ([lower[-1]] if lower else [])
                + ([upper[0]] if upper else [])]

    def branch_checks(self, state):
        for other in self.neighbors(state):
            secant = (state.z - other.z) / (state.q - other.q)
            ti, tj = other.tangent, state.tangent
            ni, nj = max(1.0, infnorm(ti)), max(1.0, infnorm(tj))
            errors = [infnorm(secant-ti), infnorm(secant-tj), infnorm(tj-ti)]
            bounds = [0.25*ni, 0.25*nj, 0.50*max(ni, nj)]
            orientations = [float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
                            for a, b in ((secant, ti), (secant, tj), (ti, tj))]
            self.emit("neighbor_branch_check", q=state.q, neighbor_q=other.q,
                      signed_h=state.q-other.q, errors=errors, bounds=bounds,
                      cosines=orientations,
                      arrays=self.audit.arrays("neighbor", secant=secant))
            require(finite(secant, errors, bounds, orientations)
                    and all(e <= b for e, b in zip(errors, bounds))
                    and all(c >= 0.5 for c in orientations),
                    "UNRESOLVED_BRANCH", q=state.q, neighbor_q=other.q,
                    errors=errors, bounds=bounds, cosines=orientations)
        seen_negative = False
        states = sorted([*self.cache.values(), state], key=lambda s: s.q)
        for item in states:
            label = sign(item.slope)
            require(not (label > 0 and seen_negative),
                    "UNRESOLVED_MULTIPLE_TURNING_BEHAVIOR", q=item.q)
            seen_negative = seen_negative or label < 0
        self.emit("derivative_order", samples=[(s.q, s.slope, sign(s.slope)) for s in states])

    def tube(self, x, q, prediction, radius):
        z = self.model.sample(x, q)
        error = infnorm(z - prediction)
        return finite(x, z, error) and error <= radius, z, error

    def solve(self, q, seed=None):
        self.budget()
        require(self.attempts < 126, "UNRESOLVED_REFINEMENT_BUDGET", attempts=self.attempts)
        require(q not in self.cache, "UNRESOLVED_Q_COLLISION", q=q)
        self.attempts += 1
        zero = seed is None
        if zero:
            require(q == 0, "UNRESOLVED_ZERO_STATE")
            x = np.zeros(self.model.n_unknowns, dtype=np.float64)
            prediction, radius = None, None
        else:
            h = q - seed.q
            require(h != 0, "UNRESOLVED_Q_COLLISION", q=q)
            x = seed.x + h * seed.xq
            prediction = seed.z + h * seed.tangent
            radius = 0.25 * abs(h) * max(1, infnorm(seed.tangent))
            inside, _, error = self.tube(x, q, prediction, radius)
            require(inside, "UNRESOLVED_BRANCH", detail="initial predictor", tube_error=error)
        self.emit("attempt", attempt=self.attempts, q=q, seed_q=None if zero else seed.q,
                  radius=radius, arrays=self.audit.arrays("prediction", x=x,
                      **({} if zero else {"z_prediction": prediction})))
        try:
            state = self.iterate(q, x, zero, prediction, radius)
        except Unresolved as error:
            if zero:
                raise Unresolved("UNRESOLVED_ZERO_STATE", cause=error.reason,
                                 cause_details=error.details) from error
            raise
        self.cache[q] = state
        self.emit("accepted", q=q, pressure=state.pressure, slope=state.slope,
                  dp_dq=self.model.p_c*state.slope, diagnostics=state.diagnostics,
                  arrays=self.audit.arrays("accepted", x=state.x, correction=state.correction,
                      xq=state.xq, z=state.z, tangent=state.tangent, residual=state.residual))
        return state

    def iterate(self, q, x, zero, prediction, radius):
        m = self.model.n_unknowns
        for iteration in range(1, 21):
            self.budget()
            energy, residual, j, fq = self.model.evaluate(x, q)
            evaluation = self.audit.arrays("evaluation", x=x, residual=residual,
                                           jacobian=j, fq=fq, energy=np.asarray(energy))
            self.emit("evaluation", q=q, iteration=iteration, arrays=evaluation)
            require(finite(energy, residual, j, fq, x), "UNRESOLVED_NONFINITE", q=q)
            if not zero:
                inside, _, error = self.tube(x, q, prediction, radius)
                require(inside, "UNRESOLVED_BRANCH", tube_error=error, q=q)
            system = LinearSystem(j)
            correction, linear_error = system.solve(-residual)
            r = infnorm(residual)
            u = infnorm(correction) / max(1, infnorm(x))
            merit = float(residual @ residual / (2*m))
            direction = float(residual @ (j @ correction) / m)
            require(finite(r, u, merit, direction), "UNRESOLVED_NONFINITE", q=q)
            diagnostics = dict(iteration=iteration, residual_inf=r, undamped_relative_inf=u,
                               merit=merit, directional_derivative=direction,
                               rcond1=system.rcond, linear_residual=linear_error)
            self.emit("iteration", q=q, energy=energy, **diagnostics,
                      evaluation=evaluation,
                      arrays=self.audit.arrays("correction", correction=correction,
                                               pivots=system.pivots))
            if r <= 1e-10 and u <= 1e-9:
                xq, slope_error = system.solve(-fq)
                z = self.model.sample(x, q)
                tangent = self.model.sample(xq, 1.0)
                require(finite(xq, z, tangent), "UNRESOLVED_BRANCH", q=q)
                require(x[-1] > 0 if q > 0 else x[-1] == 0,
                        "UNRESOLVED_PRESSURE_SIGN", q=q, pressure=x[-1])
                if zero:
                    require(xq[-1] > SLOPE_TOL, "UNRESOLVED_ZERO_STATE", slope=xq[-1])
                diagnostics["slope_linear_residual"] = slope_error
                state = State(q, x.copy(), correction, xq, z, tangent, residual, diagnostics)
                self.branch_checks(state)
                return state
            require(not zero, "UNRESOLVED_ZERO_STATE", **diagnostics)
            require(iteration < 20, "UNRESOLVED_NEWTON_BUDGET", q=q, **diagnostics)
            require(direction < 0, "UNRESOLVED_NON_DESCENT", q=q, direction=direction)
            accepted = False
            for alpha in ALPHAS:
                self.budget()
                trial = x + alpha * correction
                inside, _, error = self.tube(trial, q, prediction, radius)
                rhs = merit + 1e-4 * alpha * direction
                trial_merit = None
                arrays = dict(x=trial)
                if not inside:
                    reason = "nonfinite_or_outside_fixed_tube"
                else:
                    et, ft, _, _ = self.model.evaluate(trial, q, jacobian=False)
                    arrays["residual"] = ft
                    trial_merit = float(ft @ ft / (2*m))
                    if not finite(et, ft, trial_merit, rhs):
                        reason = "nonfinite"
                    elif trial_merit <= rhs:
                        reason, accepted = "accepted", True
                    else:
                        reason = "armijo"
                self.emit("trial", q=q, iteration=iteration, alpha=alpha, reason=reason,
                          tube_error=error, tube_radius=radius, merit=trial_merit, bound=rhs,
                          arrays=self.audit.arrays("trial", **arrays))
                if accepted:
                    x = trial
                    break
            require(accepted, "UNRESOLVED_BACKTRACKING", q=q, iteration=iteration)
        raise AssertionError("Unreachable Newton exit")

    def bracket(self, left, right):
        require(left.q < right.q and sign(left.slope) == 1 and sign(right.slope) == -1,
                "UNRESOLVED_PEAK_BRACKET", left_q=left.q, right_q=right.q,
                left_slope=left.slope, right_slope=right.slope)
        interior = [s for q, s in sorted(self.cache.items()) if left.q < q < right.q]
        require(bool(interior), "UNRESOLVED_PEAK_BRACKET", detail="no interior witness")
        # Comparing in pressure order avoids rejecting a tie among lower samples.
        # Only ambiguity at the maximum is a tie for the maximum witness.
        ordered = sorted(interior, key=lambda s: s.pressure, reverse=True)
        middle = ordered[0]
        for other in ordered[1:]:
            require(self.compare(other, middle, "maximum_witness") == 1,
                    "UNRESOLVED_PEAK_BRACKET")
        require(self.compare(left, middle, "left_witness") == 1
                and self.compare(right, middle, "right_witness") == 1,
                "UNRESOLVED_PEAK_BRACKET")
        self.emit("bracket", a=left.q, b=right.q, middle=middle.q,
                  pressures=[left.pressure, middle.pressure, right.pressure],
                  slopes=[left.slope, middle.slope, right.slope])
        return middle

    def find_coarse(self):
        self.coarse = [self.solve(0.0)]
        first_bracket = None
        descending = []
        for j in range(1, 101):
            previous = self.coarse[-1]
            current = self.solve(j / 20, previous)
            self.coarse.append(current)
            direction = self.compare(previous, current, "coarse_edge")
            if first_bracket is None:
                if direction > 0:
                    continue
                require(j >= 2, "UNRESOLVED_PEAK_BRACKET", q=current.q)
                left, middle, right = self.coarse[-3:]
                require(all(sign(s.slope) == 1 for s in self.coarse[:-2]),
                        "UNRESOLVED_PEAK_BRACKET", detail="earlier coarse slope")
                witness = self.bracket(left, right)
                require(witness is middle, "UNRESOLVED_PEAK_BRACKET")
                first_bracket = (left, middle, right)
            else:
                require(direction == -1 and sign(current.slope) == -1,
                        "UNRESOLVED_PEAK_BRACKET", detail="descending corroboration", q=current.q)
            descending.append(current)
            if len(descending) == 3:
                self.emit("descending_certificate", samples=[(s.q, s.pressure, s.slope)
                                                              for s in descending])
                return first_bracket, descending
        raise Unresolved("UNRESOLVED_Q_CEILING", last_q=self.coarse[-1].q)

    def new_refinement(self, q, left, right):
        require(left.q < q < right.q and q not in self.cache,
                "UNRESOLVED_Q_COLLISION", q=q, a=left.q, b=right.q)
        require(self.refinements < 24, "UNRESOLVED_REFINEMENT_BUDGET",
                refinements=self.refinements)
        seed = min(self.cache.values(), key=lambda s: (abs(q-s.q), s.q))
        self.refinements += 1
        state = self.solve(q, seed)
        middle = self.bracket(left, right)
        self.peaks.append(middle.pressure)
        self.emit("peak_history", refinements=self.refinements, peaks=self.peaks.copy())
        return state, middle

    def stop(self, left, middle, right):
        if self.refinements < 4 or right.q-left.q > 0.001 or self.peaks[-1] <= 0:
            return False
        span = (max(self.peaks[-4:])-min(self.peaks[-4:])) / abs(self.peaks[-1])
        self.emit("stop_certificate", width=right.q-left.q, last_four_span=span,
                  refinements=self.refinements, middle=middle.q)
        return span <= 0.001

    def run(self):
        (left, middle, right), descending = self.find_coarse()
        rho = (math.sqrt(5) - 1) / 2
        c, middle = self.new_refinement(right.q-rho*(right.q-left.q), left, right)
        d, middle = self.new_refinement(left.q+rho*(right.q-left.q), left, right)
        while not self.stop(left, middle, right):
            direction = self.compare(c, d, "golden_direction")
            if direction > 0:
                proposed_left, proposed_right = c, right
            else:
                proposed_left, proposed_right = left, d
            require(proposed_left.q < middle.q < proposed_right.q,
                    "UNRESOLVED_PEAK_BRACKET", detail="would discard highest witness")
            middle = self.bracket(proposed_left, proposed_right)
            left, right = proposed_left, proposed_right
            if self.stop(left, middle, right):
                break
            if direction > 0:
                c = d
                d, middle = self.new_refinement(left.q+rho*(right.q-left.q), left, right)
            else:
                d = c
                c, middle = self.new_refinement(right.q-rho*(right.q-left.q), left, right)
        return dict(status="CERTIFIED_NUMERICAL_PEAK", peak=middle.pressure, q=middle.q,
                    bracket=[left.q, right.q],
                    bracket_pressures=[left.pressure, middle.pressure, right.pressure],
                    bracket_slopes=[left.slope, middle.slope, right.slope],
                    peaks=self.peaks, attempts=self.attempts, refinements=self.refinements,
                    descending=[dict(q=s.q, pressure=s.pressure, slope=s.slope) for s in descending])


def sequence(model_factory, audit, budget):
    """No retry, cross-mesh seed, or later mesh after any failure."""
    results = []
    for n in (64, 128, 256):
        budget()
        audit.event("mesh_start", intervals=n)
        controller = None
        try:
            model = model_factory(n)
            controller = Continuation(model, audit, budget)
            result = controller.run()
        except Unresolved as error:
            audit.event("unresolved", intervals=n, reason=error.reason, details=error.details)
            return dict(status="UNRESOLVED", intervals=n, reason=error.reason,
                        details=error.details, completed_meshes=results,
                        attempts=controller.attempts if controller else 0,
                        refinements=controller.refinements if controller else 0)
        result["intervals"] = n
        results.append(result)
        audit.event("mesh_complete", **result)
    # Source data enter only this final postprocessing, after three certificates.
    peaks = [r["peak"] for r in results]
    changes = [abs(b-a)/abs(b) for a, b in zip(peaks, peaks[1:])]
    nominal = abs(peaks[-1]-0.250)/0.250
    endpoints = [abs(peaks[-1]-value)/value for value in (0.247, 0.253)]
    passed = all(v <= 0.01 for v in changes) and max(nominal, *endpoints) <= 0.05
    return dict(status="PASS" if passed else "FAIL", meshes=results,
                adjacent_relative_changes=changes, nominal_relative_error=nominal,
                graph_endpoint_relative_errors=endpoints,
                qualification="Builder result only; source/model qualifications persist; Una verification pending.")
