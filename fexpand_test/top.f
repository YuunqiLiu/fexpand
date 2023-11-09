

+incdir+   $PRJ_ICDIR/qwerwr
+incdir+   ./qwer
-y 2333.v
#define A C+1
#define B 9
-y $PRJ_ICDIR/fexpand
$PRJ_ICDIR/fexpand
#define OPEN_SUB
#define SUB1
#ifdef SUB1
-f $PRJ_ICDIR/fexpand_test/sub1.f
-f $PRJ_ICDIR/pcpp/../fexpand_test/sub1.f
#endif
#undef OPEN_SUB
//some comment 2
#define SUB2
#ifdef SUB2
-f $PRJ_ICDIR/../pcpp/fexpand_test/sub2.f
#endif

QWER/res-res.v
#ifdef SUB3
../res.v
#endif


