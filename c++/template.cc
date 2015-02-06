#include <stdio.h>

class Rational 
{
public:
  Rational();
  Rational(int ca = 0, int cb= 0)
    : a(ca), b(cb)
  {}
  void print()
  {
    printf("%d, %d\n", a, b);
  }
public:
  int a;
  int b;
};

const Rational operator*(const Rational& lhs, const Rational& rhs)
{
  return Rational(lhs.a + rhs.a, lhs.b + rhs.b);
}

int main(int argc, char* argv[])
{
  Rational r1(1, 2);
  Rational r2(3, 4);
  Rational r3 = r1 * r2;
  Rational r4 = r1 * 2;
  Rational r5 = 2 * r1;
  r1.print();
  r2.print();
  r3.print();
  r4.print();
  r5.print();
  return 0;
}
