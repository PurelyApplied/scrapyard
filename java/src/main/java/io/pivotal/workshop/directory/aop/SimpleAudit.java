package io.pivotal.workshop.directory.aop;

import io.pivotal.workshop.directory.annotation.Audit;
import io.pivotal.workshop.directory.annotation.Auditor;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Aspect
public class SimpleAudit {

  private static Logger log = LoggerFactory.getLogger("[AUDIT]");


  @Before("@annotation(audit)")
  public void preAudit(JoinPoint jp, Audit audit){
    log.info("[EXECUTING] " + jp.getSignature());
    if (audit.value().equals(Auditor.BEFORE) || audit.value().equals(Auditor.BEFORE_AND_AFTER)){
      log.info("[ARGS] ", jp.getArgs());
    }
  }

}
