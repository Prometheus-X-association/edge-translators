
// ==> add localisation datatype & PropertyPath property

const rdfs_DataType = 'rdfs:Datatype'

const mm_PropertyPath = 'mm:PropertyPath'

export default function createGeoDatatypeAndProperty() {

  // 1/ dataType
  const geoDataType = {
    id: 'mm:geoDataType',
    type: [rdfs_DataType],
    label: ['A DataType for serializing point for App-Search.'],
    // label: ['A DataType for Well-Known Text (WKT) serialization of a Geometry'],
    // comment: ['This is a pure DataType approch of geo:wktLiteral, where the value is only the WKT string and the coordinate reference system uri is in `.termType` property.'],
    seeAlso: 'https://opengeospatial.github.io/ogc-geosparql/geosparql11/spec.html#_rdfs_datatype_geowktliteral'
  }

  // 2/ homeLocation property for the personalDataWallet 
  const geoLocation_id = 'mms:geoLocation'
  const homeLocation = {
    id: 'mms:homeLocation',
    type: [rdfs_DataType, mm_PropertyPath],
    domain: ['mms:PersonalDataWallet'],
    range: [geoDataType.id],
    mirror: [geoLocation_id],
    subjectPath: ['mms:owner']
  }
  console.log('@TODO: implement mms:owner inverse property')


  // 3/ geoLocation property for the user's profile
  const geoLocation = {
    id: geoLocation_id,
    type: [rdfs_DataType],
    domain: ['mms:User'],
    range: [geoDataType.id],
  }


  return [geoDataType, homeLocation, geoLocation]
}