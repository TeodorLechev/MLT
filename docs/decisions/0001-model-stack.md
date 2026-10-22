# 0001 – Model stack (NumPy core vs PyTorch)
- Status: proposed (hypothesis, NOT yet tested)

## Question
Which model families and training schemes should the production path support?

## Hypothesis
Small models can run on NumPy, keeping live inference light and identical to research.
Heavier models (sequence nets, GPU) may be trained in Colab and exported (NumPy/ONNX) for live.

## Experiment (to do)
Compare linear (online and batch), small NN, gradient boosting and at least one sequence model on the SAME
data, features and costs, on a held-out period, against buy-and-hold. Accept only what beats baselines
after costs and is stable to parameter changes.
