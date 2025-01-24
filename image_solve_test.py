from CaptchaImageSolver import CaptchaImageSolver


solver = CaptchaImageSolver()

grid_size, grid_width, grid_height = solver.count_grids("captchatest.png")

print(grid_size)
