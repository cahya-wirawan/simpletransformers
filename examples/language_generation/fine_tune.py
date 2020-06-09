from simpletransformers.language_modeling import LanguageModelingModel
import logging
import argparse


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

train_args = {
    "reprocess_input_data": True,
    "overwrite_output_dir": True,
    "block_size": 512,
    "max_seq_length": 512,
    "learning_rate": 5e-6,
    "train_batch_size": 8,
    "gradient_accumulation_steps": 8,
    "num_train_epochs": 3,
    "mlm": False,
    "output_dir": f"outputs/fine-tuned/",
}

parser = argparse.ArgumentParser()
parser.add_argument("--local_rank", type=int, default=-1,
                    help="Local rank. Necessary for using the torch.distributed.launch utility.")
args = parser.parse_args()

train_args["local_rank"] = args.local_rank

model = LanguageModelingModel("gpt2", "gpt2", args=train_args)

model.train_model("data/train.txt", eval_file="data/test.txt")

model.eval_model("data/test.txt")
