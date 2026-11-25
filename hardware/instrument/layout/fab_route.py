"""fab_route.py — the order route's parts list, kept free of kiutils/numpy so the smoke test can import it.

DNP_FIRST_ARTICLES: left off the fab BOM and CPL (the footprint stays on the board, unpopulated). U7 (LIS2DW12TR) is Standard-PCBA-only and the first articles use
Economic PCBA; leaving it in makes JLC's BOM page ask about "unselected parts" at every NEXT. Reinstate it by removing it here when the Standard route is used.
"""

DNP_FIRST_ARTICLES = {"U7"}
