#include <iostream>
#include <utility>
#include <winbase.h>

int readfile(const char* str, char* stor);

class Difichento {
protected:
    char name[40];
public:
    char speech[40];
    explicit Difichento(char* n);
    virtual void get_speech() = 0;
    virtual void say() = 0;
    void tell(const char* spec) {
      printf("%s\n", spec);
    }
};


Difichento::Difichento(char* n) {
  strncpy(name, n, 40);
}

class Ivan: public Difichento{
public:
    Ivan():Difichento("Ivan") {this->get_speech();}; //I've always been doing so
    void get_speech() {
      char buf[40] = {0};
      snprintf(buf, 40, "%s%s", this->name, ".txt");
      readfile(buf, this->speech);
    }
    void say() override {
        std::cout << "I am " << this->name << std::endl;
    }
};

class Fedot: public Difichento {
public:
    Fedot():Difichento("Fedot") {this->get_speech();}; //I'll prove I'm right!
    void get_speech() {
      char buf[40] = {0};
      snprintf(buf, 40, "%s%s", this->name, ".txt");
      readfile(buf, this->speech);
    }
    void say() override {
        std::cout << "I am " << this->name << std::endl;
    }
};
class Evkakiy: public Difichento {
public:
    Evkakiy():Difichento("Evkakiy") {this->get_speech();}; //We don't have a dealer to do it
    void get_speech() {
      char buf[40] = {0};
      snprintf(buf, 40, "%s%s", this->name, ".txt");
      readfile(buf, this->speech);
    }
    void say() override {
        std::cout << "I am " << this->name << std::endl;
    }
};
