"""Download multiple pages with or without threads."""

from concurrent.futures import as_completed, ThreadPoolExecutor
from typing import Callable, List, Optional

import enlighten
from pydantic import BaseModel as Base

from .lookup import fuzzy_search


def _download_pages_without_threads(  # pylint: disable=too-many-arguments
    group_object: Base,
    callable_: Callable,
    symbols: List[str],
    use_fuzzy_search: bool,
    page_not_found_ok: bool,
    progress_bar: bool,
    **kwargs,  # noqa: ANN003
) -> Optional[Base]:

    pages = group_object()

    if use_fuzzy_search:
        valid_symbols = []

        if progress_bar:
            pbar = enlighten.Counter(
                total=len(symbols), desc="Validating symbols...", unit="symbols"
            )

        for symbol in symbols:
            result = fuzzy_search(
                symbol,
                first_ticker=True,
                **kwargs,  # session, proxies, timeout
            )

            valid_symbols.append(result)

            if progress_bar:
                pbar.update()

        valid_symbols = filter(lambda s: s is not None, valid_symbols)
        symbols = list(set(s.symbol for s in valid_symbols))

    if progress_bar:
        pbar = enlighten.Counter(
            total=len(symbols), desc="Downloading Page Data...", unit="symbols"
        )

    for symbol in symbols:
        results = callable_(
            symbol,
            use_fuzzy_search=False,
            page_not_found_ok=page_not_found_ok,
            **kwargs,  # session, proxies, timeout
        )

        if results:
            pages.append(results)

        if progress_bar:
            pbar.update()

    if len(pages) > 0:
        return pages

    return None


def _download_pages_with_threads(  # pylint: disable=too-many-arguments
    group_object: Base,
    callable_: Callable,
    symbols: List[str],
    use_fuzzy_search: bool,
    page_not_found_ok: bool,
    thread_count: int,
    progress_bar: bool,
    **kwargs,  # noqa: ANN003
) -> Optional[Base]:
    pages = group_object()

    if use_fuzzy_search:
        valid_symbols = []

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(
                    fuzzy_search,
                    symbol,
                    first_ticker=True,
                    **kwargs,
                    # kwargs for requestor: session, proxies, timeout
                )
                for symbol in symbols
            ]

            if progress_bar:
                pbar = enlighten.Counter(
                    total=len(futures), desc="Validating symbols...", unit="symbols"
                )

            for future in as_completed(futures):
                valid_symbols.append(future.result())

                if progress_bar:
                    pbar.update()

        valid_symbols = filter(lambda s: s is not None, valid_symbols)
        symbols = list(set(s.symbol for s in valid_symbols))

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        futures = [
            executor.submit(
                callable_,
                symbol,
                use_fuzzy_search=False,
                page_not_found_ok=page_not_found_ok,
                **kwargs,
                # kwargs for requestor: session, proxies, timeout
            )
            for symbol in symbols
        ]

        if progress_bar:
            pbar = enlighten.Counter(
                total=len(futures), desc="Downloading Page Data...", unit="symbols"
            )

        for future in as_completed(futures):
            results = future.result()

            if results:
                pages.append(results)

            if progress_bar:
                pbar.update()

    if len(pages) > 0:
        return pages

    return None
