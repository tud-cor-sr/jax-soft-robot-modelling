from jax import numpy as jnp
from jax import Array, lax, jit


@jit
def blk_diag(a: Array) -> Array:
    """
    Create a block diagonal matrix from a tensor of blocks
    Args:
        a: matrices to be block diagonalized of shape (m, n, o)

    Returns:
        b: block diagonal matrix of shape (m * n, m * o)

    """

    def assign_block_diagonal(i, _b):
        """
        Save the ith block  into the block-diagonal matrix `_b`
        Args:
            i: Index of block which we save into the block-diagonal matrix.
            _b: Block diagonal matrix. Should still have zeros at the ith block.
        Returns
        """
        # Assign the block saved in ith entry of `a` to the ith block-diagonal of `_b`
        # Hint: use `jax.lax.dynamic_update_slice` to update the entries of `_b`
        _b = lax.dynamic_update_slice(
            operand=_b, update=a[i], start_indices=(i * a.shape[1], i * a.shape[2])
        )
        return _b

    # Implement for loop to assign each block in `a` to the block-diagonal of `b`
    # Hint: use `jax.lax.fori_loop` and pass `assign_block_diagonal` as an argument
    b = jnp.zeros((a.shape[0] * a.shape[1], a.shape[0] * a.shape[2]))
    b = lax.fori_loop(
        lower=0,
        upper=a.shape[0],
        body_fun=assign_block_diagonal,
        init_val=b,
    )

    return b
