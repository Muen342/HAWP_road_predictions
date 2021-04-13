First download and unzip the CULane dataset zip into the root directory of hawp

Rename the folder to temp and run renameAll.py. This is such that when all the images and data are pulled into the same directory, no data is lost.

cd into that directory and run $find . -mindepth 2 -type f -print -exec mv {} . \;

then type mv * ../data/wireframe/images

To load node you need to load the modules
Module load StdEnv/2020
Module load nodejs/12.16.1

run $node create_train_set.js to get train.json. Move this to data/wireframe/
run $node create_val_set.js to get val.json. Move this to data/wireframe/
run $node create_test.js to get test.json. Move this to data/wireframe/

When training use $sbatch run_train.sh

When checking the training loss or validation loss, rename whichever test set you would like to use as the train test set to be train.json in data/wireframe/ and run $sbatch run_train_test.sh

It will output the loss of each epoch on the specified dataset for a sample of 500 batches or 3000 images (batch size of 6)

If you want to get the val loss, rename train.json to something else temporarily and rename val.json to train.json