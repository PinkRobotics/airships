import {planStatusText} from '../sim/index.js?v=6f3787a9';
import {esc} from './dom.js?v=6f3787a9';
export const inactiveText=m=>planStatusText({state:m.planState,reason:m.planReason});
export const figure=(m,quantity,value,text,basis='record')=>`<span data-energy-quantity="${quantity}" data-energy-value="${value}" data-energy-basis="${basis}" data-plan-hull="${esc(m.name)}">${text}</span>`;
