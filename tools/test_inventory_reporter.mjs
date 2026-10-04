/* Terminal Node test events: actual names and files, including explicit skips.
 * Only native 3D suites use this reporter; shared cases publish their harness record.
 */
export default async function* inventory(source) {
  for await (const event of source) {
    if (event.type === 'test:pass' || event.type === 'test:fail') {
      yield JSON.stringify(event) + '\n';
    }
  }
}
