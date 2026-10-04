/* Data adapter for the independent equations. */
import * as S from '../../sim/index.js?v=979323dd';
export const loadTree=async()=>({S,which:'integrated'});
export const sum=o=>Object.values(o).reduce((a,b)=>a+b,0);
export function norm(_,s){return {surplusT:s.surplusT,bagT:s.owners.bagT,rotorT:s.owners.rotorT,aeroT:s.owners.aeroT,
 vdragDownT:s.owners.verticalDragT,inertiaDownT:0,unheldT:s.unheldT,rotorCapT:s.thrustLimitT,aeroCapT:s.aeroLimitT,
 busMW:s.busMW,gross:sum(s.draw),rotorsMW:s.draw.rotors,draw:s.draw,gen:s.gen,feasible:s.feasible,limits:s.limits,
 airV:s.airV,vz:s.vz,alt:s.alt,massT:s.massT,liftT:s.led.liftT,rho:s.led.rho,hoistMW:s.hoistMW,rotorAskMW:s.rotorAskMW,gs:s.gs,water:s.water};}
export const planInfo=(_,p)=>({feasible:p.feasible,worstT:p.worst.unheldT,worstPhase:p.worst.phase,worstProg:p.worst.progress});
