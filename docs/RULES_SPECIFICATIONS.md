# 📘 Mapping Rules Documentation (Valid JSON Format)

This document contains mapping rules grouped by class, formatted as valid JSON. Click on 'Show Rule' to expand each rule.

Each object will have a Rule to handle ID generation: 

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Profile",
  "generateId": true
}
```

## 🔹 Profile

### `name`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Profile",
  "targetProperty": "soo:name"
}
```

### `email`


```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Profile",
  "targetProperty": "soo:email"
}
```

### `address`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Profile",
  "targetProperty": "soo:address"
}
```

## 🔹 Experience

### `prefLabel`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetFunction": "fno:search-for-mapping-with-source",
  "targetFunctionParam": "",
  "targetLang": "en",
  "targetProperty": "skos:prefLabel"
}
```

### `description`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:description"
}
```

### `dateFrom`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:dateFrom",
  "targetFunction": "fno:date-to-xsd",
  "targetFunctionParam": "",
  "- (choice1) fno": "big-endian-no-separator",
  "- (choice2) fno": "year-only"
}
```

### `dateTo`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:dateTo",
  "targetFunction": "fno:date-to-xsd",
  "targetFunctionParam": "",
  "- (choice1) fno": "big-endian-no-separator",
  "- (choice2) fno": "year-only"
}
```

### `company`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:company"
}
```

### `location`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:location"
}
```

### `contractType`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:contractType"
}
```

### `family`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:family"
}
```

### `sourceId`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:sourceId"
}
```

### `polarity`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:polarity"
}
```

### `sourceDataValue`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Experience",
  "targetProperty": "soo:sourceDataValue"
}
```

## 🔹 Skill

### `prefLabel`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Skill",
  "targetFunction": "fno:search-for-mapping-with-source",
  "targetLang": "en",
  "targetProperty": "skos:prefLabel"
}
```

### `description`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Skill",
  "targetProperty": "soo:description"
}
```

### `category`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Skill",
  "targetProperty": "soo:category"
}
```

### `skilLevelValue`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Polarity",
  "targetProperty": "soo:value",
  "targetFunction": "fno:get-polarity-value",
  "relationTo": "soo:Skill",
  "relationName": "soo:skill",
  "relationNameInverse": "soo:polarity"
}
```

### `SourceSkillId`

```json
{
  "id": "mmr:rule-{id}",
  "sourcePath": "{sourcePath}",
  "targetClass": "soo:Skill",
  "targetProperty": "soo:sourceSkillId"
}
```
