
#include <iostream>
#include "zbar.h"
#include <opencv2/opencv.hpp>

int main(int argc, char*argv[])
{
  zbar::ImageScanner scanner;
  scanner.set_config(zbar::ZBAR_NONE, zbar::ZBAR_CFG_ENABLE, 1);
  cv::Mat image = cv::imread(argv[1]);
  cv::Mat imageGray;
  cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
  int width = image.cols;
  int height = image.rows;
  uchar *raw = (uchar *)image.data;
  zbar::Image imageZbar(width, height, "Y800", raw, width*height);
  scanner.scan(imageZbar); //扫描条码  
  zbar::Image::SymbolIterator symbol = imageZbar.symbol_begin();
  if (imageZbar.symbol_begin() == imageZbar.symbol_end())
  {
    std::cout << "查询条码失败，请检查图片！" << std::endl;
  }
  for (; symbol != imageZbar.symbol_end(); ++symbol)
  {
    std::cout << "类型：" << symbol->get_type_name() << std::endl;
    std::cout << "条码：" << symbol->get_data() << std::endl;
  }
  cv:imwrite("test.jpg", image);
  return 0;
}
