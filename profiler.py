import pstats

p = pstats.Stats('./output.prof')
p.sort_stats('calls').print_stats(10)
p.sort_stats('cumulative').print_stats(10)
