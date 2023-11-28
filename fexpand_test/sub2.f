-f $PRJ_ICDIR/fexpand_test/test2/sub1.f
#ifdef SUB2
$PRJ_ICDIR/open_sub2.v

`endif


`ifdef OPEN_SUB
$PRJ_ICDIR/open_sub2.v

`endif

$PRJ_ICDIR/sub2.v