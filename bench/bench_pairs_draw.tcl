# Same workload in DRAWEXE: bcommon on each pair listed in pairs.txt.
# Usage: DRAWEXE -v -f bench_pairs_draw.tcl -- BREP_DIR PAIRS_FILE
pload MODELING
set dir $env(BENCH_DIR)
set pf $env(BENCH_PAIRS)
set fh [open $pf r]; set pairs {}
while {[gets $fh line] >= 0} {lappend pairs $line}
close $fh
set loaded {}
foreach p $pairs {
    foreach n $p {
        if {[lsearch $loaded $n] < 0} {restore $dir/$n.brep $n; lappend loaded $n}
    }
}
set t0 [clock microseconds]
foreach p $pairs {
    set a [lindex $p 0]; set b [lindex $p 1]
    bcommon rr $a $b
}
puts [format "%d pairs  %.2f s" [llength $pairs] [expr {([clock microseconds]-$t0)/1e6}]]
exit
