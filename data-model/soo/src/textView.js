
export default function textView(ld, stripNs = true) {

  const lines = []
  const classes = ld.graph.filter(e => e.type?.includes('rdfs:Class'))

  for (const cl of classes) {
    // @TODO: use getApiLabel function
    const clName = stripNs ? cl.id.split(':')[1] : cl.id
    lines.push('', `# ${clName}`)
    const properties = ld.graph.filter(e => e?.domain?.includes(cl.id))

    for (const prop of properties) {
      const propName = stripNs ? prop.id.split(':')[1] : prop.id
      const line = `${clName} --${propName}--> ${prop.range.join(' | ')}`
      lines.push(line)
    }

  }

  const txt = lines.join('\n')
  return txt
}