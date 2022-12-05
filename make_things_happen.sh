#!/usr/bin/env bash




# generate graph
#python make_graph.py


anonymity_level=0
for i in {1..5}
do

  echo "Run $i"

  cp JIT-defect-models/dataset/wildfly_metrics.csv JIT-defect-models/dataset/wildfly_metrics_${anonymity_level}.csv
  latest_file_name=$(ls -t bug_annonted* | head -1)
  echo "$latest_file_name"
  cp "$latest_file_name" JIT-defect-models/dataset/wildfly_metrics.csv
  cd JIT-defect-models
  python train_global_model.py wildfly RF

  cd ../
  #python anonymise_run.py



  anonymity_level=$(($anonymity_level+20))
  echo $anonymity_level

done

# anonymise data x amount

#bug_annonted-

# generate stats & bug annotation
# run prediction
# save results



