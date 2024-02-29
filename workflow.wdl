version development

workflow sfkit {
  input {
    String study_id
    Directory? data
    Int num_cores = 16 # TODO: test with smaller CP0
    String api_url = "https://sfkit.dsde.broadinstitute.org/api"
    String docker = "us-central1-docker.pkg.dev/dsp-artifact-registry/sfkit/sfkit"
  }

  call cli {
    input:
      study_id = study_id,
      data = data,
      num_cores = num_cores,
      api_url = api_url,
      docker = docker,
  }
}

task cli {
  input {
    String study_id
    Directory? data
    Int num_cores
    String api_url
    String docker
  }

  Float mem_gb = num_cores * 8 * 1000.0 / 1024

  command <<<
      set -xeu

      export PYTHONUNBUFFERED=TRUE
      export SFKIT_PROXY_ON=true
      export SFKIT_API_URL="~{api_url}"
      cd /sfkit

      sfkit auth --study_id "~{study_id}"
      sfkit networking
      sfkit generate_keys

      if [ -n "~{data}" ]; then
        sfkit register_data --data_path "~{data}"
      fi

      sfkit run_protocol
  >>>

  runtime {
    docker: docker
    cpu: num_cores
    memory: "~{mem_gb} GB"
  }

  output {
    String out = read_string(stdout())
  }
}
