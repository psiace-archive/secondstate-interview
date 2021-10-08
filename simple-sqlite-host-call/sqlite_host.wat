(module
  (type $t0 (func (param i32) (result i32)))
  (import "extern" "func-sqlite" (func $f-sqlite (type $t0)))
  (func (export "visit_sqlite") (param i32) (result i32)
    local.get 0
    call $f-sqlite)
)
