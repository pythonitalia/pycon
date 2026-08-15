from unittest.mock import call, patch

import strawberry

from cms.api.page.registry import REGISTRY, get_block_union


def test_get_block_union_imports_blocks_in_sorted_order():
    @strawberry.type
    class FirstBlock:
        value: str

    @strawberry.type
    class SecondBlock:
        value: str

    with (
        patch(
            "glob.glob",
            return_value=[
                "api/cms/page/blocks/second.py",
                "api/cms/page/blocks/first.py",
            ],
        ),
        patch("importlib.import_module") as import_module,
        patch.dict(
            REGISTRY,
            {"first": FirstBlock, "second": SecondBlock},
            clear=True,
        ),
    ):
        get_block_union()

    assert import_module.call_args_list == [
        call("cms.api.page.blocks.first"),
        call("cms.api.page.blocks.second"),
    ]
