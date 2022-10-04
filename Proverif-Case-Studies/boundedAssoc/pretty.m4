ifdef(`allFlat',`(* All flattening that make sense for the given protocol! *)
')dnl
ifdef(`noFlat',`(* No flattening! *)
')dnl
ifdef(`noCol',`(* No collision! *)
')dnl
ifdef(`allCol',`(* No prevention of collisions on small values! *)
')dnl
ifdef(`refl',`(* No prevention of reflection attack *)
')dnl
ifdef(`noRole',`(* No explicit authentication on the agent role through signature. *)
')dnl
ifdef(`noCook',`(* No cookie mechanism. *)
')dnl
ifdef(`noCook',`(* With cookie only. *)
')dnl
ifdef(`IPC',`(* No CPC but IPC (identical prefix collisions) only! *)
')dnl
ifdef(`boundedCol',`(* Only bounded CPC or IP-C (on prefix of size 1 block)! *)
')dnl
