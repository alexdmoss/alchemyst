import sys
import pdftotree


if __name__ == '__main__':
    pdftotree.parse(sys.argv[1], html_path=None, model_type=None, model_path=None, favor_figures=True, visualize=False)


#pip install pylzma
