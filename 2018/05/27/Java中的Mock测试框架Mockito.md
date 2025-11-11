---
title: "Java中的Mock测试框架Mockito"
date: 2018-05-27
tags:
  - Java
  - Mockito
  - 单元测试
description: "上周无意中了解到一个很有意思的Java mock测试套件Mockito，简单研究了下，感觉拿来写单元测试和集成测试应该很好用，而且用起来也很方便，话不多说，直接看代码。 1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950515253545556575859606162"
---

# Java中的Mock测试框架Mockito

<div class="article-meta">
  <span class="date">📅 发布于：2018年05月27日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Java</span> <span class="tag">Mockito</span> <span class="tag">单元测试</span></span>
</div>

上周无意中了解到一个很有意思的Java mock测试套件Mockito，简单研究了下，感觉拿来写单元测试和集成测试应该很好用，而且用起来也很方便，话不多说，直接看代码。

```text
packagecom.mockedtesting;

importstaticjunit.framework.TestCase.assertTrue;
importstaticorg.junit.Assert.assertEquals;
importstaticorg.junit.Assert.assertFalse;
importstaticorg.mockito.Mockito.*;

importjava.util.ArrayList;
importjava.util.Iterator;
importjava.util.List;
importjava.util.NoSuchElementException;

importorg.junit.Test;

publicclassMockedObjectUnitTest{

@Test
publicvoidtestMock(){
List mockedList = mock(List.class);

mockedList.add("one");
mockedList.add("two");
mockedList.add("three times");
mockedList.add("three times");
mockedList.add("three times");
when(mockedList.size()).thenReturn(100);
assertEquals(mockedList.size(),100);

// as you see, load and clear
verify(mockedList, atLeastOnce()).add("one");
verify(mockedList, times(1)).add("two");
verify(mockedList, times(3)).add("three times");
verify(mockedList, never()).isEmpty();
}

@Test
publicvoidcreateMockObject(){
List mockedList = mock(List.class);
assertTrue(mockedListinstanceofList);

ArrayList mockedArrayList = mock(ArrayList.class);
assertTrue(mockedArrayListinstanceofList);
assertTrue(mockedArrayListinstanceofArrayList);
}

@Test
publicvoidconfigMockObject(){
List mockedList = mock(List.class);

// CONFIG: when calling mockedList.add("one"), return true
when(mockedList.add("one")).thenReturn(true);

// CONFIG: when calling mockedList.size(), return 1
when(mockedList.size()).thenReturn(1);

assertTrue(mockedList.add("one"));
// Because there's no config for mockedList.add("two"), false is
// returned as default value
assertFalse(mockedList.add("two"));
assertEquals(mockedList.size(),1);

Iterator i = mock(Iterator.class);

// CONFIG: when calling i.next(), return "Hello," at 1st time,
// return "Mockito" at 2nd time
when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");
String result = i.next() +" "+ i.next();
assertEquals("Hello, Mockito!", result);
}

@Test(expected = NoSuchElementException.class)
publicvoidtestForException()throwsException{
Iterator i = mock(Iterator.class);
when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");
String result = i.next() +" "+ i.next();
assertEquals("Hello, Mockito!", result);

// CONFIG: throw exception when calling i.next() for the 3rd time,
// which means only 2 elements in i.
doThrow(newNoSuchElementException()).when(i).next();
i.next();// now it is the 3rd time to call i.next()
}
}

```