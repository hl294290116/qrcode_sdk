file(REMOVE_RECURSE
  "libzbar.pdb"
  "libzbar.a"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/zbar.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
