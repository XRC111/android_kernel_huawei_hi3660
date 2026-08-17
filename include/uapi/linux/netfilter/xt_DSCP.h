/* x_tables module for DSCP field (combined header for Windows case-insensitive FS)
 *
 * Contains: XT_DSCP_* macros, xt_dscp_info/xt_tos_match_info (match),
 *           xt_DSCP_info/xt_tos_target_info (target)
 */
#ifndef _XT_DSCP_H_COMBINED
#define _XT_DSCP_H_COMBINED

#include <linux/types.h>

#define XT_DSCP_MASK	0xfc	/* 11111100 */
#define XT_DSCP_SHIFT	2
#define XT_DSCP_MAX	0x3f	/* 00111111 */

/* match info (xt_dscp.h) */
struct xt_dscp_info {
	__u8 dscp;
	__u8 invert;
};

struct xt_tos_match_info {
	__u8 tos_mask;
	__u8 tos_value;
	__u8 invert;
};

/* target info (xt_DSCP.h) */
struct xt_DSCP_info {
	__u8 dscp;
};

struct xt_tos_target_info {
	__u8 tos_value;
	__u8 tos_mask;
};

#endif /* _XT_DSCP_H_COMBINED */
