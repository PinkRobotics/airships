# Natural Resources Canada — Photovoltaic Potential and Solar Resource Maps of Canada

Open Government Licence – Canada. The municipality database (`municip_kWh.csv`) was downloaded and
read directly; the figures below are computed from it, not quoted from a summary.

## What it establishes

Mean daily global insolation, in kWh per square metre per day, by month, for over 3,500 Canadian
municipalities on a roughly 2 km grid, in six array orientations: horizontal, four fixed
south-facing tilts, and two-axis sun tracking. Insolation data are from Environment and Climate
Change Canada; the product is maintained with CanmetENERGY.

For July, across eight municipalities in the British Columbia interior fire belt — Cranbrook,
Kamloops, Kelowna, Merritt, Penticton, Prince George, Vernon and Williams Lake — the mean daily
global insolation on a **horizontal** surface is **6.34 kWh/m²/day**, ranging from 5.87 at Prince
George to 6.58 at Cranbrook. On a two-axis tracker, which no airship hull can be, the same set
averages 9.4 kWh/m²/day.

## Why it cuts against us

`sim/state.js` line 351 reads `const gen = { solar: cls.solarM2 * 200 / 1e6 };`. That is 200 W/m²
of **electrical output**, applied continuously through every phase of every cycle, with no time of
day, no cloud, no latitude and no surface orientation. The literal is not in `sim/config.js` with
the other assumptions; it is hard-coded in the state module.

6.34 kWh/m²/day is 264 W/m² of incident energy averaged over 24 hours. Getting 200 W/m² of
electricity out of that requires a conversion efficiency of **76%**. Commercial silicon modules
reach 20–23%; the record for any laboratory cell under concentration is below 50%. Even against
the two-axis tracking figure the hull cannot achieve, 200 W/m² needs 51% efficiency.

Put the other way round, at 20% module efficiency the same insolation yields about **53 W/m²**
day-averaged, and about 87 W/m² if you credit only the roughly sixteen daylight hours of a BC July
and take 22%. The model's solar term is between 2.3 and 3.8 times too large depending on how
generously it is read, and it is not close on any reading.

This makes the README's sustainment problem worse, not better, which is the direction that matters:
solar per cycle currently offsets 0.68, 3.3 and 18.2 MWh on the three classes, and correcting it
would move most of that back into the deficit `selftest()` already asserts must stay visible.

## Where it does not settle the question

The dataset gives insolation on flat surfaces at ground level. An airship at 2,500 m is above a
meaningful fraction of the atmospheric column and above most low cloud, so its incident irradiance
is higher than the municipal figure — by perhaps 10–20% at this altitude, not by a factor of four.
Against that, a hull is a curved body: only a fraction of `solarM2` faces anywhere near the sun at
any moment, and the cosine losses on a cylinder are large. The dataset also cannot say what smoke
above an active fire does to irradiance, which is a real and probably substantial further
reduction that nobody in this collection has quantified.
