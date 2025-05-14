
export default function createClass(id) {
  return {
    id,
    type: ['rdfs:Class', 'owl:Class'],
  }
}