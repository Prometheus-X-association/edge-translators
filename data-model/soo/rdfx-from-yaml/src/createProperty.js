export default function createProperty(property) {
  const _type = ['rdf:Property']
  
  let { id, type, domain, range, ...rest } = property
  if (!type) type = _type
  range = Array.isArray(range) ? range : [range]
  return {
    id,
    type,
    domain,
    range,
    ...rest,
  }
}