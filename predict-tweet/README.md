# predict-tweet
Based on yusuketomoto's [chainer-char-rnn](https://github.com/yusuketomoto/chainer-char-rnn)


## Requirement
- [Chainer](https://github.com/pfnet/chainer)
```
$ pip install chainer
$ pip install chainer-cuda-deps
```

## Train
Start training the model using `train.py`, for example

```
$ python train.py
```

The `--data_dir` flag specifies the dataset to use. By default it is set to `data/tinyshakespeare` which consists of a subset of works of Shakespeare.

**Your own data**: If you'd like to use your own data create a single file `input.txt` and place it into a folder in `data/`. For example, `data/some_folder/input.txt`.

## Tweets Data
Data for the entire collection of your past tweets can be found on [Twitter](https://twitter.com/settings/account). When the data is ready, download it to a suitable location.

It is a zipped CSV file, containing metadata such as timestamp as well as the tweet body. To make the text data compatible with train.py, perform some processing so that you get one single file containing all of your tweets, possibly line-separated.


## Sampling
Given a checkpoint file (such as those written to cv) we can generate new text. For example:
```
$ python sample.py \
--vocabulary data/tinyshakespeare/vocab.bin \
--model cv/some_checkpoint.chainermodel \
--primetext some_text --gpu -1
```
## References
- Original implementation: https://github.com/karpathy/char-rnn
- Blog post: http://karpathy.github.io/2015/05/21/rnn-effectiveness/
