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
