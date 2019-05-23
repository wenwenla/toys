#include <bits/stdc++.h>
using namespace std;

/*
 * E3 -> E3 + E2 | E3 - E2 | E2
 * E2 -> E2 * E1 | E2 / E1 | E1
 * E1 -> E0 ^ E1 | E0
 * E0 -> (E3) | number
 * */

/*
 * E3 -> E2 E3'
 * E3' -> + E2 E3' | - E2 E3' | eps
 *
 * E2 -> E1 E2'
 * E2' -> * E1 E2' | / E1 E2' | eps
 *
 * E1 -> E0 ^ E1 | E0
 *
 * E0 -> (E3) | number
 * */

double e3(); double e2(); double e1(); double e0();
struct Buffer {
    string line;
    int pos;
    bool read() { pos = 0; return bool(cin >> line); }
    char peek() { return pos < line.size() ? line[pos] : -1; }
    char get() { char t = peek(); ++pos; return t; }
} buf;
double e3() {
    double ans = e2();
    while(true) {
        char op = buf.peek();
        if(op == '+') {
            buf.get();
            ans += e2();
        } else if(op == '-') {
            buf.get();
            ans -= e2();
        } else {
            break;
        }
    }
    return ans;
}

double e2() {
    double ans = e1();
    while(true) {
        char op = buf.peek();
        if(op == '*') {
            buf.get();
            ans *= e1();
        } else if(op == '/') {
            buf.get();
            ans /= e1();
        } else {
            break;
        }
    }
    return ans;
}

double e1() {
    double ans = e0();
    char op = buf.peek();
    if(op == '^') {
        buf.get();
        ans = pow(ans, e1());
    }
    return ans;
}

double e0() {
    double ans = 0.0;
    char op = buf.peek();
    if(op == '(') {
        buf.get();
        ans = e3();
        buf.get();
    } else {
        string token;
        char d;
        do {
            token += buf.get();
            d = buf.peek();
        } while(d >= '0' && d <= '9' || d == '.');
        stringstream ss(token);
        ss >> ans;
    }
    return ans;
}

int main() {
    while(buf.read()) {
        double ans = e3();
        printf("%f\n", ans);
    }
    return 0;
}
