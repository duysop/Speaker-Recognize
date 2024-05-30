# **speaker identification**

Speaker identification with Vietnamese.


# **Contents**
- [Overview](#overview)
- [Installation](#installation)
- [Settings](#settings)
- [Dataset](#dataset)
- [Training](#training)
- [Evaluate](#evaluate)

# **Overview**
a project to identification "who is talking" in Vietnamese voice using WavLM-large

# **Installation**

## *Create environment*

1. Install miniconda or anaconda.
2. Create conda environment

    ```bash
    conda create -n SID python=3.9.5
    conda activate SID
    ```


## *Install dependencies*

1. Important Dependencies
    ```bash
    pip install -r requirements.txt
    ```

# **Settings**

_n_gpu=2,
accelerator_config={'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True},
adafactor=False,
adam_beta1=0.9,
adam_beta2=0.999,
adam_epsilon=1e-08,
auto_find_batch_size=False,
bf16=False,
bf16_full_eval=False,
data_seed=None,
dataloader_drop_last=False,
dataloader_num_workers=0,
dataloader_persistent_workers=False,
dataloader_pin_memory=True,
dataloader_prefetch_factor=None,
ddp_backend=None,
ddp_broadcast_buffers=None,
ddp_bucket_cap_mb=None,
ddp_find_unused_parameters=None,
ddp_timeout=1800,
debug=[],
deepspeed=None,
disable_tqdm=False,
dispatch_batches=None,
do_eval=True,
do_predict=False,
do_train=False,
eval_accumulation_steps=None,
eval_delay=0,
eval_steps=400,
evaluation_strategy=steps,
fp16=False,
fp16_backend=auto,
fp16_full_eval=False,
fp16_opt_level=O1,
fsdp=[],
fsdp_config={'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False},
fsdp_min_num_params=0,
fsdp_transformer_layer_cls_to_wrap=None,
full_determinism=False,
gradient_accumulation_steps=1,
gradient_checkpointing=False,
gradient_checkpointing_kwargs=None,
greater_is_better=None,
group_by_length=False,
half_precision_backend=auto,
hub_always_push=False,
hub_model_id=None,
hub_private_repo=False,
hub_strategy=every_save,
hub_token=<HUB_TOKEN>,
ignore_data_skip=False,
include_inputs_for_metrics=False,
include_num_input_tokens_seen=False,
include_tokens_per_second=False,
jit_mode_eval=False,
label_names=None,
label_smoothing_factor=0.0,
learning_rate=5e-05,
length_column_name=length,
load_best_model_at_end=False,
local_rank=0,
log_level=passive,
log_level_replica=warning,
log_on_each_node=True,
logging_dir=test-trainer/runs/Apr25_04-45-39_cf4356e838ea,
logging_first_step=False,
logging_nan_inf_filter=True,
logging_steps=400,
logging_strategy=steps,
lr_scheduler_kwargs={},
lr_scheduler_type=linear,
max_grad_norm=1.0,
max_steps=-1,
metric_for_best_model=None,
mp_parameters=,
neftune_noise_alpha=None,
no_cuda=False,
num_train_epochs=4,
optim=adamw_torch,
optim_args=None,
optim_target_modules=None,
output_dir=test-trainer,
overwrite_output_dir=False,
past_index=-1,
per_device_eval_batch_size=8,
per_device_train_batch_size=4,
prediction_loss_only=False,
push_to_hub=False,
push_to_hub_model_id=None,
push_to_hub_organization=None,
push_to_hub_token=<PUSH_TO_HUB_TOKEN>,
ray_scope=last,
remove_unused_columns=False,
report_to=['tensorboard', 'wandb'],
resume_from_checkpoint=None,
run_name=test-trainer,
save_on_each_node=False,
save_only_model=False,
save_safetensors=True,
save_steps=500,
save_strategy=steps,
save_total_limit=None,
seed=42,
skip_memory_metrics=True,
split_batches=None,
tf32=None,
torch_compile=False,
torch_compile_backend=None,
torch_compile_mode=None,
torchdynamo=None,
tpu_metrics_debug=False,
tpu_num_cores=None,
use_cpu=False,
use_ipex=False,
use_legacy_prediction_loop=False,
use_mps_device=False,
warmup_ratio=0.0,
warmup_steps=0,
weight_decay=0.0,

# **Dataset**
    Dataset of 30 VietNamese speaker with total 15 hours speak
## *Downloading data*
Dataset can be download at [Driver](https://drive.google.com/file/d/1POEVZSWE0v0oz14y055c8SoOUtnrS04r/view?usp=drive_link)

## *Create training & testing dataset*
    run file WavLM/wavlm.ipynb

# **Training**
    run file WavLM/wavlm.ipynb

# **Evaluate**
    *Metric
        Accuracy_score ( In multilabel classification, this function computes subset accuracy: the set of labels predicted for a sample must exactly match the corresponding set of labels in y_true )
![Screenshot 2024-05-22 000234](https://github.com/duysop/Speaker-Recognize/assets/103120531/b182b072-a34a-4f14-8c8b-63d416b669d3)

