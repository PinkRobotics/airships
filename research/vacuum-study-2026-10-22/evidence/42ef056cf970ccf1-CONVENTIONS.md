# MAINLINE-050 night transient: implementation conventions

Response to q-ref-fb5fd651ac3cba87c03d. This is an equation-only clarification of the already-filed calculation, not a new calculation or a change to its results. All inherited material values remain QUESTIONABLE and the night predictions remain PROJECTION. The original package is unchanged.

## Dry storage and reference geometry

Each of the two thermal compartments has the same dry heat capacity per unit hull area:

\[
C_o=C_i=C=t_f(1850)(1825)+\tfrac12t_c(16.018463373960138)(900)
\quad\mathrm{J\,m^{-2}K^{-1}}.
\]

Each compartment contains one beryllium face and **half** the honeycomb core metal. The two compartments together contain both faces and the full core. No adhesive, polymer, primer, coating, mooring-pad, systems or cavity-gas heat capacity is included. This omission reduces modeled dry storage; it is not a general proof of conservative condensate mass. Deposited water/ice storage is additional and enters only the outer compartment's enthalpy inversion.

Yes: the night geometries are precisely the five **mask 11, usage 1 ISA reference rows** in MASS-CURVES.json, including the low-emissivity and heating evaluations and the R=10 sensitivity cases. The geometry is fixed across the night weather cases. It is not reoptimized for the night and is not drawn from the later FIXED-HULLS product.

| R (m) | One face thickness, tf (m) | Core thickness, tc (m) | C per compartment (J/m²/K) |
|---|---|---|---|
| 10 | 0.0008094863689461697 | 0.022361237087042612 | 2894.2150489283595 |
| 12 | 0.0009715822271487676 | 0.026825833225638075 | 3473.6733765614076 |
| 15 | 0.0012148391094282064 | 0.03351837854250005 | 4343.211356773887 |
| 20 | 0.0016205306721411878 | 0.04466250358308 | 5793.257786842403 |
| 30 | 0.00243284836732763 | 0.06691492493843312 | 8696.247723623825 |

These reference structures were designed at 97172.30184301017 Pa. **That structural pressure is not the pressure in the night mass-transfer expression.**

## Outer enthalpy and vapor reference

Let Tf=273.15 K, m be deposited mass per hull area (kg/m²), and E the outer areal enthalpy (J/m²). The zero of E is the dry outer compartment and all deposited material as ice at Tf.

Use cp,ice=2100, cp,water=4180 and cp,vapor=1860 J/kg/K, fusion heat Lf=334000 J/kg, and sublimation heat Ls=2835000 J/kg.

\[
T_o=\begin{cases}
T_f+E/(C+m c_{p,\mathrm{ice}}),& E<0,\\
T_f,&0\le E\le mL_f,\\
T_f+(E-mL_f)/(C+m c_{p,\mathrm{water}}),&E>mL_f.
\end{cases}
\]

Liquid mass per area is clip(E/Lf,0,m); the remainder is ice. At m=0 the dry sensible-heat relation is recovered.

Incoming vapor has specific enthalpy

\[
h_v(T_a)=L_s+c_{p,\mathrm{vapor}}(T_a-T_f).
\]

At Tf it lies Ls above ice and Ls−Lf=2501000 J/kg above liquid. A deposited increment dm adds hv(Ta) dm to E **once**. There is no second latent-heat source. Inner storage is C(Ti−Tf).

Initially E=C(Ta−Tf), Ti=Ta, and m=0. No preexisting wet film, evaporation or shedding is modeled. All positive deposition is retained.

## Ambient pressure, saturation and Lewis relation

Every night case and radius uses the constant ambient pressure

\[
P_0=95460.83791390515\ \mathrm{Pa}.
\]

This is also used for air density in forced convection. Let RD=287.053 and RV=461.5 J/kg/K, cp,air=1005 J/kg/K, and Le=0.87.

\[
e_a=RH_{\mathrm{water}}e_{s,w}(T_a),\qquad
\rho_a=(P_0-0.378e_a)/(R_DT_a).
\]

RH is relative to liquid water, including the cold-frost case. For c=T−273.15 in degrees Celsius:

\[
e_{s,w}(T)=611.21\exp[(18.678-c/234.5)c/(257.14+c)],
\]
\[
e_{s,i}(T)=611.15\exp[(23.036-c/333.7)c/(279.82+c)]
\quad\mathrm{Pa}.
\]

Use ice saturation at old To<Tf and water saturation at old To≥Tf:

\[
j=\max(e_a-e_s(T_o),0)\,
\frac{h(R_D/R_V)}{c_{p,\mathrm{air}}P_0}\,Le^{-2/3}
\quad\mathrm{kg\,m^{-2}s^{-1}}.
\]

For completeness, convection is evaluated pointwise from the old outer temperature:

\[
Re=\rho_a v(2R)/(1.79\,10^{-5}),
\]
\[
h_{\mathrm{forced}}=
\frac{0.0257}{2R}\,
\left[2+(0.4\sqrt{Re}+0.06Re^{2/3})0.71^{0.4}\right],
\]
\[
h=h_{\mathrm{scale}}\max\!\left(
h_{\mathrm{forced}},\,
1.32\max(|T_o-T_a|,0.05)^{1/4}
\right).
\]

The base hscale is 1. The material and correlation constants are the inherited implementation values.

## Through-core heat transfer

Let μi and wi be Gauss–Legendre abscissae and weights on [−1,1]. The area-average weights are ai=wi/2, summing to one. The mean used in the through-core coefficient is the **old inner skin's area-weighted temperature**, not an outer/inner arithmetic mean:

\[
\overline T_i=\sum_i a_i T_i,\qquad
U=\frac{130(16.018463373960138)}{2700t_c}
+0.8\sigma_{\mathrm{SB}}\overline T_i^{\,3}.
\]

U has units W/m²/K and σSB=5.670374419×10⁻⁸ W/m²/K⁴. The first term is the inherited solid-aluminum conductivity times the core metal volume fraction divided by thickness. The second is the inherited linearized radiative term, with 0.8=4×0.2, evaluated at the old inner mean.

\[
q_{c,i}=U(T_{o,i}-T_{i,i})
\]

is positive into the inner compartment. Separate inner-cavity radiation redistributes heat:

\[
q_{\mathrm{int},i}=0.2\sigma_{\mathrm{SB}}
\left(T_{i,i}^{4}-\sum_j a_j T_{i,j}^{4}\right).
\]

Its area integral vanishes. External heat into the outer compartment is

\[
T_{\mathrm{env},i}^{4}
=\tfrac12(1+\mu_i)T_{\mathrm{sky}}^4
+\tfrac12(1-\mu_i)T_a^4,
\]
\[
q_{\mathrm{ext},i}
=-\epsilon\sigma_{\mathrm{SB}}(T_{o,i}^4-T_{\mathrm{env},i}^4)
-h_i(T_{o,i}-T_a).
\]

Emissivity is fixed: 0.8 in the base cases and 0.05 in the low-emissivity sensitivity. Condensate does not change the optics.

## Time and phase update order

This is forward Euler with every right-hand-side quantity frozen at the **old** state:

1. Decode To,n and liquid mass from En,mn.
2. Compute saturation, jn, hn, the inner mean, Un, qc,n, qint,n and qext,n from the old temperatures. Ambient conditions stay fixed.
3. Let dm=jn Δt.
4. Update En+1=En+(qext,n−qc,n)Δt+hv(Ta)dm.
5. Update Ti,n+1=Ti,n+(qc,n−qint,n)Δt/C.
6. Update mn+1=mn+dm.

Sequential assignment does not cause a later right-hand side to use an already-updated state. There is no implicit, midpoint or predictor step. Phase is decoded again from the updated E,m for recorded output and on the next step/final evaluation.

Base runs are 12 hours, 64 angular zones and requested Δt=5 s. The step count is round(duration/requested Δt), and the actual step is duration divided by that count. The refinement uses 128 zones and requested Δt=2.5 s. Histories use post-update states, every max(1,N//24) steps and at the final step, with timestamps (step+1)Δt.

## Provenance

The owner checked these conventions against the original, sealed implementation. No implementation source is attached to this clarification, preserving the checker's requested independent reconstruction.

Original non-code output pins:

- MASS-CURVES.json: 664796 bytes, SHA-256 68aa030d82c0cb9f3e8a9b85e687a8e2dd354cc0615316f393b320b89313de4f.
- DEW-FROST.json: 527908 bytes, SHA-256 8abf5b23e80fc72590cc1986f26f8afc6e8745bd4ffe7881b54b33e8115e1f03.
- METHOD.md: 8577 bytes, SHA-256 809696d0f6797c69402379f83e0619742991547290afbbf722bba2f10d626d8a.

The source directory is the owner's .ship/work/outputs/vacuum-mainline050-flyable-weather-1020. This clarification changes none of those files and provides no new validation claim.
