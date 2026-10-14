/* Bounded analysis worker: identical selector and exact inputs, local data only. */
import {CLASSES} from '../../sim/index.js?v=3c39c29e';
import {acceptedLogistics} from './accepted-logistics.js';
self.onmessage = ({data}) => {
  try {
    self.postMessage({rows:data.legs.map(leg => ({...leg,
      ...acceptedLogistics(CLASSES[data.class],leg.km)}))});
  } catch (error) { self.postMessage({error:error.message}); }
};
