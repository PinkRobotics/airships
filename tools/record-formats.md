# Bounded generated records

The solar movement record remains plain JSON. Its metadata and values are kept
verbatim. `files` gives the file table. Each movement row is an array containing
the file index, common-prefix length against that file's previous field path,
remaining path suffix, old value, new value, and the precision when present.
Each list starts with empty previous paths. List order is retained.

`tools/record_energy_fix.py` owns both the writer and
`expand_solar_record(record)`, which recovers the former object rows and metadata.
The existing percent encoding stays in those expanded paths; decode it once to
recover source keys. `tools/convert_records.py --part solar` converts a former
record, proves canonical equality before writing and leaves identical bytes
untouched. `--baseline` compares with a separately saved original record.

The claims carry history keeps `files`, `headlines`, `retired`, `added` and
`defect_changes` unchanged. A revalidated row now stores `id` and `changed`,
whose keys name changed fields and whose pairs give exact old and new values.
Unchanged fields are omitted. `tools/claims.py` owns `compact_carry_run(run)`,
which reads either form and returns those exact changed-field pairs.
`tools/convert_records.py --part carry` converts every former run, including a
history containing both forms, and proves preservation before writing.

The claims register and served-inertia record retain their complete JSON values.
Their writers put each top-level entry or analysis row on its own line without
indentation inside rows. Existing JSON readers continue to parse them directly.
The shared energy writer and the claims JSON writer compare bytes before writing.
`tools/convert_records.py --part register` reformats an existing register with a
canonical equality proof. The served-inertia producer owns its row format.
