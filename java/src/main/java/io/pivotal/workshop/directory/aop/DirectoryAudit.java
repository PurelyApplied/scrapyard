package io.pivotal.workshop.directory.aop;

import java.util.stream.IntStream;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.pivotal.workshop.directory.annotation.Audit;
import io.pivotal.workshop.directory.config.DirectoryProperties;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class DirectoryAudit {

  private DirectoryProperties props;

  public DirectoryAudit(DirectoryProperties props){
    this.props = props;
  }

  private static Logger log = LoggerFactory.getLogger("[D-AUDIT]");

  @Around("execution(* *(..)) && @annotation(audit)")
  public Object audit(ProceedingJoinPoint jp, Audit audit) throws Throwable {
    Object[] args = jp.getArgs();

    this.printBar();
    this.print("[executing] " + (props.getInfo().toLowerCase().equals("short") ? jp.getSignature().getName() : jp.getSignature() ));

    switch (audit.value()) {
      case BEFORE:
      case BEFORE_AND_AFTER:
        this.printArgs(args);
      default:
        break;
    }

    Object obj = jp.proceed(args);

    switch (audit.value()) {
      case AFTER:
      case BEFORE_AND_AFTER:
        this.print("[result] " + obj);
      default:
        this.printBar();
        break;
    }

    return obj;
  }

  private void print(Object obj) {
    log.info(obj.toString());
  }

  private void printArgs(Object[] args) {
    IntStream.range(0, args.length).forEach(idx -> {
      log.info(String.format("[params] arg%d = %s", idx, args[idx]));
    });

  }

  private void printBar(){
    log.info("===========");
  }
}
