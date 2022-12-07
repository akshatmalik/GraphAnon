#!/usr/bin/env bash


find . -type f -name "bug_annonted-*" -print0 | while IFS= read -r -d '' file; do
    echo "file = $file"

    cp "$file" JIT-defect-models/dataset/wildfly_metrics.csv
    cd JIT-defect-models
    echo "RF"
    python train_global_model.py wildfly RF
    echo "LR"
    python train_global_model.py wildfly LR
    cd ../



done