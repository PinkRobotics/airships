/* Straight-route track kinematics, separate from force-and-bus feasibility.
 * Boundary cases use stipulated test inputs, never incident operating limits. */
export function trackWind(selectedAirKph, wind = null) {
  if (!(Number.isFinite(selectedAirKph) && selectedAirKph > 0))
    throw new RangeError('Selected airspeed must be positive and finite');
  // Without a route bearing the vector cannot be projected onto a track.
  const windUsed = wind != null && wind.bearing != null;
  if (windUsed && !(Number.isFinite(wind.spd) && wind.spd >= 0 &&
                   Number.isFinite(wind.dir) && Number.isFinite(wind.bearing)))
    throw new RangeError('Route wind requires finite speed, direction and bearing');
  const angle = windUsed ? ((wind.dir + 180) % 360 - wind.bearing) * Math.PI / 180 : 0;
  const tailOut = windUsed ? wind.spd * Math.cos(angle) : 0;
  const gsOut = selectedAirKph + tailOut, gsRet = selectedAirKph - tailOut;
  const trackReason = !(gsOut > 0) ? 'outbound leg has no positive ground speed at selected airspeed'
    : !(gsRet > 0) ? 'return leg has no positive ground speed at selected airspeed' : null;
  return {selectedAirKph, gsOut, gsRet, tailOut, windUsed, trackPossible: trackReason === null, trackReason};
}
