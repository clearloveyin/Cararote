class car{
    constructor(name) {
        this.name = name
    }
    getInfo (){//car的一般方法
        console.log(this.name);

        return this.name
        
    }
    static show(){//car的静态方法show
        console.log('car');
        
    }
    
}

class bmw extends car{
    constructor(name,type){
        super(name)//调用父类的构造方法
        this.type = type
    }
    getInfo2(){
        return super.getInfo()//返回父类的方法getInfo
    }
    static show2(){
        return super.show()
    }
}