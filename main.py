from canvas import Canvas


def main():
    canvas = Canvas()    
    canvas.filled_triangle((0, 100), (100, -50), (-100, -50), (255, 255, 255))
    canvas.show()


if __name__ == "__main__": main()