# Frozen-feature input schema

`scripts/run_precomputed.py` consumes one outer-fold NPZ with these fields:

| Field | Shape | Meaning |
|---|---|---|
| `source_odd` | `[n_me, c, t]` | odd projection of ME features |
| `source_even` | `[n_me, c, t]` | even projection of ME features |
| `source_y` | `[n_me]` | binary ME labels, encoded 0/1 |
| `target_odd` | `[n_mi, c, t]` | odd projection of MI features |
| `target_even` | `[n_mi, c, t]` | even projection of MI features |
| `target_y` | `[n_mi]` | binary MI labels, encoded 0/1 |
| `support_idx` | `[n_support]` | labelled target indices used for fitting |
| `query_idx` | `[n_query]` | outer-query indices scored after fitting |

The support and query indices must be disjoint and the support must contain both
classes. Query labels are accepted only for post-fit evaluation; changing them
must not change the returned scores.
