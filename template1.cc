#include <iostream>

template<typename T>
class Rational;

template<typename T>
const Rational<T> doMultiply(const Rational<T>& , const Rational<T>&);

template<typename T>
class Rational 
{
public:
  Rational<T>(T ca, T cb)
    : a(ca), b(cb)
  {}
  void print()
  {
    std::cout << a << "," << b << std::endl;
  }
  friend const Rational<T> operator*(const Rational<T>& lhs, const Rational<T>& rhs)
  {
    return doMultiply(lhs, rhs);
  }
public:
  T a;
  T b;
};

template<typename T>
const Rational<T> doMultiply(const Rational<T>& lhs, const Rational<T>& rhs)
{
  return Rational<T>(lhs.a + lhs.a, lhs.b + rhs.b);
}

int main(int argc, char* argv[])
{
  Rational<int> r1(1, 2);
  Rational<int> r2(3, 4);
  Rational<int> r3 = r1 * r2;
  Rational<double> r4(10.0, 20.0);
  Rational<double> r5 = r4 * r4;
  r1.print();
  r2.print();
  r3.print();
  r4.print();
  r5.print();
  return 0;
}
