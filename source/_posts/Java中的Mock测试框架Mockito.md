---
title: Java中的Mock测试框架Mockito
date: 2018-05-27 21:15:05
tags: [Java, Mockito, 单元测试]
---

上周无意中了解到一个很有意思的Java mock测试套件Mockito，简单研究了下，感觉拿来写单元测试和集成测试应该很好用，而且用起来也很方便，话不多说，直接看代码。

``` java
package com.mockedtesting;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;

import org.junit.Test;

public class MockedObjectUnitTest {

    @Test
    public void testMock() {
        List mockedList = mock(List.class);

        mockedList.add("one");
        mockedList.add("two");
        mockedList.add("three times");
        mockedList.add("three times");
        mockedList.add("three times");
        when(mockedList.size()).thenReturn(100);
        assertEquals(mockedList.size(), 100);

        // as you see, load and clear
        verify(mockedList, atLeastOnce()).add("one");
        verify(mockedList, times(1)).add("two");
        verify(mockedList, times(3)).add("three times");
        verify(mockedList, never()).isEmpty();
    }

    @Test
    public void createMockObject() {
        List mockedList = mock(List.class);
        assertTrue(mockedList instanceof List);

        ArrayList mockedArrayList = mock(ArrayList.class);
        assertTrue(mockedArrayList instanceof List);
        assertTrue(mockedArrayList instanceof ArrayList);
    }

    @Test
    public void configMockObject() {
        List mockedList = mock(List.class);

        // CONFIG: when calling mockedList.add("one"), return true
        when(mockedList.add("one")).thenReturn(true);

        // CONFIG: when calling mockedList.size(), return 1
        when(mockedList.size()).thenReturn(1);

        assertTrue(mockedList.add("one"));
        // Because there's no config for mockedList.add("two"), false is 
        // returned as default value
        assertFalse(mockedList.add("two"));
        assertEquals(mockedList.size(), 1);

        Iterator i = mock(Iterator.class);

        // CONFIG: when calling i.next(), return "Hello," at 1st time,
        // return "Mockito" at 2nd time
        when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");
        String result = i.next() + " " + i.next();
        assertEquals("Hello, Mockito!", result);
    }

    @Test(expected = NoSuchElementException.class)
    public void testForException() throws Exception {
        Iterator i = mock(Iterator.class);
        when(i.next()).thenReturn("Hello,").thenReturn("Mockito!");
        String result = i.next() + " " + i.next();
        assertEquals("Hello, Mockito!", result);

        // CONFIG: throw exception when calling i.next() for the 3rd time,
        // which means only 2 elements in i.
        doThrow(new NoSuchElementException()).when(i).next();
        i.next(); // now it is the 3rd time to call i.next()
    }
}
```
