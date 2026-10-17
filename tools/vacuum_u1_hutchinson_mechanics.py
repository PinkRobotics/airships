"""Frozen Hutchinson dimple energy and analytic original-coordinate derivatives.

The source qualifications and numerical protocol live beside the benchmark.
No equilibrium is computed by this module's import or operator construction.
"""

import math

import numpy as np
from scipy.interpolate import CubicSpline


EPSILON = 0.01
NU = 0.3
B = 1.5
END = math.pi / 2
PC = 2 * EPSILON**2 / math.sqrt(3 * (1 - NU**2))
GAMMA = PC / EPSILON
BETA = B / math.sqrt(math.sqrt(1 - NU**2) / EPSILON)


class Operators:
    """Natural cubic cardinal bases and exact integrated V basis."""

    def __init__(self, intervals):
        self.intervals = intervals
        self.nodes = np.linspace(0.0, END, intervals + 1)
        self.spline = CubicSpline(self.nodes, np.eye(intervals + 1)[:, 1:-1],
                                  axis=0, bc_type="natural")
        self.primitive = self.spline.antiderivative()
        abscissae, weights = np.polynomial.legendre.leggauss(16)
        h = END / intervals
        self.points = ((self.nodes[:-1, None] + self.nodes[1:, None]) / 2
                       + h * abscissae[None, :] / 2).ravel()
        self.weights = np.tile(weights * h / 2, intervals)
        self.samples = np.sort(np.concatenate((self.nodes, self.points)))

    def at(self, points):
        points = np.asarray(points)
        return (self.spline(points), self.spline(points, 1),
                self.primitive(points) - self.primitive(END))


class Shell:
    """Discrete Psi and its gradient/Hessian with respect to a=(U,V,Wp)."""

    p_c = PC

    def __init__(self, intervals):
        self.ops = Operators(intervals)
        self.n_unknowns = 2 * intervals - 1
        self.n_interior = intervals - 1
        shape, derivative, integral = self.ops.at(self.ops.points)
        zeros = np.zeros_like(shape)
        last = np.zeros((len(shape), 1))
        self.u = np.column_stack((shape, zeros, last))
        v = np.column_stack((zeros, shape, last))
        self.w = np.column_stack((zeros, integral, np.ones_like(last)))
        du = np.column_stack((derivative, zeros, last))
        self.phi = self.u - v
        self.linear_theta = self.w + du
        self.omega = self.w - np.tan(self.ops.points)[:, None] * self.u
        kt = np.column_stack((derivative, -derivative, last))
        ko = -np.tan(self.ops.points)[:, None] * self.phi
        self.weights = self.ops.weights * np.cos(self.ops.points)
        w = self.weights[:, None]
        self.bending = EPSILON**2 / (12 * (1 - NU**2)) * (
            kt.T @ (w * (kt + NU * ko)) + ko.T @ (w * (ko + NU * kt)))
        self.omega_hessian = self.omega.T @ (w * self.omega)
        distance = self.ops.points - END
        self.wi_prime = (2 * EPSILON * distance / BETA**2
                         * np.exp(-(distance / BETA)**2))
        self.load = GAMMA * (self.w.T @ self.weights)
        self.sample_shape, _, self.sample_integral = self.ops.at(self.ops.samples)

    def original(self, a, pressure, hessian=True):
        """Return Psi,F,H at fixed lambda; analytic expressions allow complex checks."""
        a = np.asarray(a)
        phi = self.phi @ a
        et = self.linear_theta @ a + 0.5 * phi**2 - self.wi_prime * phi
        eo = self.omega @ a
        gt = self.linear_theta + (phi - self.wi_prime)[:, None] * self.phi
        nt = (et + NU * eo) / (1 - NU**2)
        no = (eo + NU * et) / (1 - NU**2)
        energy = (self.weights @ (et**2 + eo**2 + 2 * NU * et * eo)
                  / (2 * (1 - NU**2)) + 0.5 * a @ self.bending @ a
                  + pressure * (self.load @ a))
        residual = (gt.T @ (self.weights * nt)
                    + self.omega.T @ (self.weights * no)
                    + self.bending @ a + pressure * self.load)
        if not hessian:
            return energy, residual, None
        combined = gt + NU * self.omega
        h = (combined.T @ (self.weights[:, None] / (1 - NU**2) * combined)
             + self.omega_hessian + self.bending
             + self.phi.T @ ((self.weights * nt)[:, None] * self.phi))
        return energy, residual, h

    def evaluate(self, x, q, jacobian=True):
        a = np.concatenate((EPSILON * x[:-1], np.atleast_1d(-EPSILON * q)))
        energy, residual, h = self.original(a, x[-1], hessian=jacobian)
        if not jacobian:
            return energy, residual, None, None
        j = np.column_stack((EPSILON * h[:, :-1], self.load))
        fq = -EPSILON * h[:, -1]
        return energy, residual, j, fq

    def sample(self, x, q):
        """Z=(q,lambda,U/epsilon,V/epsilon,W/epsilon), interleaved over Q.

        This same linear map gives T when called with xq and q'=1.
        There are no pole divisions in these endpoint diagnostics.
        """
        n = self.n_interior
        u = self.sample_shape @ x[:n]
        v = self.sample_shape @ x[n:2*n]
        w = -q + self.sample_integral @ x[n:2*n]
        return np.concatenate((np.array([q, x[-1]]),
                               np.column_stack((u, v, w)).ravel()))
