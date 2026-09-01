# Time a boolean op on two .brep files inside DRAWEXE (any OCCT version).
# Usage: DRAWEXE -v -f bench_draw.tcl -- A.brep B.brep cut 3
#   (older DRAWEXE: set env A=... B=... OP=cut N=3 then -f bench_draw.tcl)
set a [lindex $argv 0]; set b [lindex $argv 1]
set op [lindex $argv 2]; if {$op eq ""} {set op cut}
set n  [lindex $argv 3]; if {$n  eq ""} {set n 3}
set times {}
for {set i 0} {$i < $n} {incr i} {
    restore $a sa
    restore $b sb
    set t0 [clock microseconds]
    switch $op {
        cut    {bcut    r sa sb}
        fuse   {bfuse   r sa sb}
        common {bcommon r sa sb}
    }
    lappend times [expr {([clock microseconds] - $t0) / 1e6}]
    unset -nocomplain r; catch {erase}
}
set times [lsort -real $times]
puts [format "%.3f" [lindex $times [expr {$n / 2}]]]
exit
