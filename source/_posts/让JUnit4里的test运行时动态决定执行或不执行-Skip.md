---
title: '让JUnit4里的test运行时动态决定执行或Skip'
date: 2018-01-16 17:34:55
tags: [Java, Junit4]
---
# Part One

一组应用了Junit4的测试，需要增加一个动态判断，来决定是否跑test。我知道这组测试其实已经应用了junit的Category功能，来做测试组的初期分类，在跑这一整套测试的时候，执行环节会针对不同的被测产品给出一个custom参数，测试代码跑起来后会根据这个custom的值，来选择排除某些category和包括哪些category。

现在这个策略不够用了，因为之前标记好的category，同一个分类下还是有动态选择执行的需求，于是这次用到了Junit4中rule特性。

下面代码就实现了一个JUnit4中的rule。

``` java
package com.ibm.robot.web.util;

import com.ibm.robot.web.util.WebPropertiesLoader;
import org.junit.rules.TestRule;
import org.junit.runner.Description;
import org.junit.runners.model.Statement;

public class NotRun5gCase implements TestRule {
    @Override
    public Statement apply(final Statement base, final Description description) {
        return new Statement() {
            @Override
            public void evaluate() throws Throwable {
                String methodName = description.getMethodName();
                loader = new WebPropertiesLoader();
                String ap_2g = loader.getString("WIFI.ap.2G", "unknow");
                String ap_5g = loader.getString("WIFI.ap.5G", "unknow");
                if (!(ap_2G.equals(ap_5G) && methodName.contains("5GHz"))) {
                        base.evaluate();
                }
            }
        };
    }
}
```
从代码中可见，这条rule规定当ap_2g的值与ap_5g相等，同时test的方法名中包含5GHz的话，则不执行这个test。 然后把这条rule应用到具体的test中即可。

``` java
public class WiFiTest{
	
	@Rule
	public TestRule notRun5gCase = new NotRun5gCase ();

	@Before
	public void setUp() throws Exception {
		System.out.println("setup actions");
	}

	@After
	public void tearDown() throws Exception {
		System.out.println("tearDown actions");
	}

	@Test
	public void testWiFi2GHz() {
		//to test wi-fi 2g
	}

	@Test
	public void testWiFi5GHz() {
		//to test wi-fi 5g
	}
}
```

# Part Two

其实还是上次的问题，在上一篇中提到解决办法是应用JUnit4里的Rule来实现，今天继续研究了下，觉得还是不够好，因为实际需求是，需要在运行测试的时候去动态skip某些test，今天请教了下一位朋友，就有了如下代码：

``` java
package com.junit4test;

import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(MyRunner.class)
public class AprilTest {

	@Test
	public void test1() {
		assert("abc".equals("abc"));
	}
	
	@Test
	public void test2() {
		assert("abc".equals("abc"));
	}
	
	@Test
	public void test3() {
		assert("abc".equals("abc"));
	}

}

```

``` java
package com.junit4test;

import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.model.FrameworkMethod;
import org.junit.runners.model.InitializationError;

public class MyRunner extends BlockJUnit4ClassRunner {

	public MyRunner(Class<?> klass) throws InitializationError {
		super(klass);
	}
	
	@Override
	protected boolean isIgnored(FrameworkMethod child) {
		if (child.getName().contains("3")) { // 此处可做动态判断，来觉得是否skip该test
			return true;
		} else {
			return false;
		}
	}

}
```
