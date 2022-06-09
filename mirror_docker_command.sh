docker run --entrypoint="" 
  --rm -w ${start_working_directory} 
  -v ${local_mount}:${server_mount}
  ${image_url}:${version}
  repo sync -j4
