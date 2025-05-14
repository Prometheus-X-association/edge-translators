import { saveJson } from "@mmorg/fsutils";
import hash from 'object-hash'

export default function saveIfChanges(target, old, path){
  const target_hash = hash(target)
  const old_hash = hash(old)
  if(target_hash === old_hash){
    console.log('No change for this file, no writes.', path)
    return 
  }
  saveJson(target, path)
}