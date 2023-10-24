from typing import Any, Callable
import tensorflow as tf
from check_shapes import check_shapes

from gpflow.base import TensorType
from gpflow.likelihoods import Gaussian


def assert_params_false(
    called_method: Callable[..., Any],
    **kwargs: bool,
) -> None:

    errors_str = ", ".join(f"{param}={value}" for param, value in kwargs.items() if value)
    if errors_str:
        raise NotImplementedError(
            f"{called_method.__qualname__} does not currently support: {errors_str}"
        )


@check_shapes(
    "K: [batch..., N, N]",
    "likelihood_variance: [broadcast batch..., broadcast N]",
    "return: [batch..., N, N]",
)
def add_noise_cov(K: tf.Tensor, W: tf.Tensor, likelihood_variance: TensorType) -> tf.Tensor:

    k_diag = tf.linalg.diag_part(K)
    return tf.linalg.set_diag(K, k_diag + likelihood_variance*(W**-2))


@check_shapes(
    "K: [batch..., N, N]",
    "X: [batch..., N, D]",
    "return: [batch..., N, N]",
)
def add_likelihood_noise_cov(K: tf.Tensor, W: tf.Tensor, likelihood: Gaussian, X: TensorType) -> tf.Tensor:

    return add_noise_cov(K, tf.squeeze(W, axis=-1), tf.squeeze(likelihood.variance_at(X), axis=-1))

